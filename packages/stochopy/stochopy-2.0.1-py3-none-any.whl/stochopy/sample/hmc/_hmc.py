import numpy

from .._common import in_search_space
from .._helpers import SampleResult, register

__all__ = [
    "sample",
]


def sample(
    fun,
    bounds,
    x0=None,
    args=(),
    maxiter=100,
    nleap=10,
    stepsize=0.01,
    seed=None,
    jac=None,
    finite_diff_abs_step=1.0e-4,
    constraints=None,
    return_all=True,
):
    """
    Sample the variable space using the Hamiltonian (Hybrid) Monte-Carlo algorithm.

    Parameters
    ----------
    fun : callable
        The objective function to be sampled. Must be in the form ``f(x, *args)``, where ``x`` is the argument in the form of a 1-D array and args is a tuple of any additional fixed parameters needed to completely specify the function.
    bounds : array_like
        Bounds for variables. ``(min, max)`` pairs for each element in ``x``, defining the finite lower and upper bounds for the sampling argument of ``fun``. It is required to have ``len(bounds) == len(x)``. ``len(bounds)`` is used to determine the number of parameters in ``x``.
    x0 : array_like or None, optional, default None
        Initial sample. Array of real elements of size (``ndim``,), where ``ndim`` is the number of independent variables.
    args : tuple, optional, default None
        Extra arguments passed to the objective function.
    maxiter : int, optional, default 100
        Total number of samples to generate.
    nleap : int, optional, default 10
        Number of leap-frog steps.
    stepsize : scalar or array_like, optional, default 0.01
        Leap-frog step size (as a fraction of feasible space defined by ``bounds``).
    perc : scalar, optional, default 1.0
        Number of dimensions to perturb at each iteration (as a fraction of total number of variables).
    seed : int or None, optional, default None
        Seed for random number generator.
    jac : callable or None, optional, default None
        Method for computing the gradient vector. If it is a callable, it should be a function in the form  ``jac(x, *args)`` that returns the gradient vector where ``x`` is an array with shape (``ndim``,) and ``args`` is a tuple with the fixed parameters. If ``None``, the gradient will be estimated using 2-point finite difference estimation with an absolute step size.
    finite_diff_abs_step : scalar, optional, default 1.0e-4
        The absolute step size to use for numerical approximation of the jacobian.
    constraints : str or None, optional, default None
        Constraints definition:

         - None: no constraint
         - 'Reject': infeasible solutions are always rejected

    return_all : bool, optional, default True
        Set to True to return an array with shape (``maxiter``, ``ndim``) of all the samples.

    Returns
    -------
    :class:`stochopy.sample.SampleResult`
        The sampling result represented as a :class:`stochopy.sample.SampleResult`. Important attributes are:

         - ``x``: the best sample array
         - ``fun``: the best sample function value
         - ``xall``: the samples array
         - '`funall``: the samples' function value array

    References
    ----------
    .. [1] S. Duane, A. D. Kennedy, B. J. Pendleton and D. Roweth, *Hybrid Monte Carlo*, Physics Letters B., 1987, 195(2): 216-222
    .. [2] N. Radford, *MCMC Using Hamiltonian Dynamics*, Handbook of Markov Chain Monte Carlo, Chapman and Hall/CRC, 2011

    """
    # Cost function
    if not hasattr(fun, "__call__"):
        raise TypeError()

    fun = count(fun)  # Wrap to count the number of function evaluations

    # Dimensionality and search space
    if numpy.ndim(bounds) != 2:
        raise ValueError()

    ndim = len(bounds)
    lower, upper = numpy.transpose(bounds)

    # Initial guess x0
    if x0 is not None and len(x0) != ndim:
        raise ValueError()

    # Number of leap-frog steps
    if nleap < 1:
        raise ValueError()

    # Step size
    if numpy.ndim(stepsize) == 0:
        stepsize = numpy.full(ndim, stepsize)

    if len(stepsize) != ndim:
        raise ValueError()

    stepsize *= 0.5 * (upper - lower)

    # Jacobian
    if not (jac is None or hasattr(jac, "__call__")):
        raise TypeError()

    if jac is None:
        jac = lambda x: numerical_gradient(x, fun, args, finite_diff_abs_step)
    else:
        jac = lambda x: jac(x, *args)

    # Seed
    if seed is not None:
        numpy.random.seed(seed)

    # Initialize arrays
    xall = numpy.empty((maxiter, ndim))
    funall = numpy.empty(maxiter)
    xall[0] = x0 if x0 is not None else numpy.random.uniform(lower, upper)
    funall[0] = fun(xall[0], *args)

    # Leap-frog algorithm
    n_accepted = 0
    for i in range(1, maxiter):
        q = xall[i - 1].copy()
        p = numpy.random.randn(ndim)  # Random momentum
        q0 = q.copy()
        p0 = p.copy()

        p -= 0.5 * stepsize * jac(q)  # First half momentum step
        q += stepsize * p  # First full position step
        for _ in range(nleap):
            p -= stepsize * jac(q)  # Momentum
            q += stepsize * p  # Position
        p -= 0.5 * stepsize * jac(q)  # Last half momentum step

        accept = False
        if in_search_space(q, lower, upper, constraints):
            U0 = fun(q0, *args)
            K0 = 0.5 * numpy.square(p0).sum()
            U = fun(q, *args)
            K = 0.5 * numpy.square(p).sum()

            log_alpha = min(0.0, U0 - U + K0 - K)
            accept = log_alpha > numpy.log(numpy.random.rand())

        if accept:
            n_accepted += 1
            xall[i] = q
            funall[i] = U
        else:
            xall[i] = xall[i - 1]
            funall[i] = funall[i - 1]

    idx = numpy.argmin(funall)
    res = SampleResult(
        x=xall[idx],
        fun=funall[idx],
        nfev=fun.nfev,
        nit=maxiter,
        accept_ratio=n_accepted / maxiter,
    )
    if return_all:
        res["xall"] = xall
        res["funall"] = funall

    return res


def count(fun):
    """Wrap objective function to count the number of function calls."""

    def wrapper(*args, **kwargs):
        wrapper.nfev += 1

        return fun(*args, **kwargs)

    wrapper.nfev = 0

    return wrapper


def numerical_gradient(x, fun, args, finite_diff_abs_step):
    """Approximate gradient vector."""
    ndim = len(x)
    x1 = x.copy()
    x2 = x.copy()

    grad = numpy.empty(ndim)
    for i in range(ndim):
        x1[i] -= finite_diff_abs_step
        x2[i] += finite_diff_abs_step

        grad[i] = fun(x2, *args) - fun(x1, *args)

        x1[i] += finite_diff_abs_step
        x2[i] -= finite_diff_abs_step

    return 0.5 * grad / finite_diff_abs_step


register("hmc", sample)
