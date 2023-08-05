# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np

from astropy.utils.decorators import deprecated_renamed_argument

__all__ = ['jackknife_resampling', 'jackknife_stats']
__doctest_requires__ = {'jackknife_stats': ['scipy']}


def jackknife_resampling(data):
    """ Performs jackknife resampling on numpy arrays.

    Jackknife resampling is a technique to generate 'n' deterministic samples
    of size 'n-1' from a measured sample of size 'n'. Basically, the i-th
    sample, (1<=i<=n), is generated by means of removing the i-th measurement
    of the original sample. Like the bootstrap resampling, this statistical
    technique finds applications in estimating variance, bias, and confidence
    intervals.

    Parameters
    ----------
    data : numpy.ndarray
        Original sample (1-D array) from which the jackknife resamples will be
        generated.

    Returns
    -------
    resamples : numpy.ndarray
        The i-th row is the i-th jackknife sample, i.e., the original sample
        with the i-th measurement deleted.

    References
    ----------
    .. [1] McIntosh, Avery. "The Jackknife Estimation Method".
        <http://people.bu.edu/aimcinto/jackknife.pdf>

    .. [2] Efron, Bradley. "The Jackknife, the Bootstrap, and other
        Resampling Plans". Technical Report No. 63, Division of Biostatistics,
        Stanford University, December, 1980.

    .. [3] Jackknife resampling <https://en.wikipedia.org/wiki/Jackknife_resampling>
    """  # noqa

    n = data.shape[0]
    if n <= 0:
        raise ValueError("data must contain at least one measurement.")

    resamples = np.empty([n, n-1])

    for i in range(n):
        resamples[i] = np.delete(data, i)

    return resamples


@deprecated_renamed_argument('conf_lvl', 'confidence_level', '4.0')
def jackknife_stats(data, statistic, confidence_level=0.95):
    """ Performs jackknife estimation on the basis of jackknife resamples.

    This function requires `SciPy <https://www.scipy.org/>`_ to be installed.

    Parameters
    ----------
    data : numpy.ndarray
        Original sample (1-D array).
    statistic : function
        Any function (or vector of functions) on the basis of the measured
        data, e.g, sample mean, sample variance, etc. The jackknife estimate of
        this statistic will be returned.
    confidence_level : float, optional
        Confidence level for the confidence interval of the Jackknife estimate.
        Must be a real-valued number in (0,1). Default value is 0.95.

    Returns
    -------
    estimate : numpy.float64 or numpy.ndarray
        The i-th element is the bias-corrected "jackknifed" estimate.

    bias : numpy.float64 or numpy.ndarray
        The i-th element is the jackknife bias.

    std_err : numpy.float64 or numpy.ndarray
        The i-th element is the jackknife standard error.

    conf_interval : numpy.ndarray
        If ``statistic`` is single-valued, the first and second elements are
        the lower and upper bounds, respectively. If ``statistic`` is
        vector-valued, each column corresponds to the confidence interval for
        each component of ``statistic``. The first and second rows contain the
        lower and upper bounds, respectively.

    Examples
    --------
    1. Obtain Jackknife resamples:

    >>> import numpy as np
    >>> from astropy.stats import jackknife_resampling
    >>> from astropy.stats import jackknife_stats
    >>> data = np.array([1,2,3,4,5,6,7,8,9,0])
    >>> resamples = jackknife_resampling(data)
    >>> resamples
    array([[2., 3., 4., 5., 6., 7., 8., 9., 0.],
           [1., 3., 4., 5., 6., 7., 8., 9., 0.],
           [1., 2., 4., 5., 6., 7., 8., 9., 0.],
           [1., 2., 3., 5., 6., 7., 8., 9., 0.],
           [1., 2., 3., 4., 6., 7., 8., 9., 0.],
           [1., 2., 3., 4., 5., 7., 8., 9., 0.],
           [1., 2., 3., 4., 5., 6., 8., 9., 0.],
           [1., 2., 3., 4., 5., 6., 7., 9., 0.],
           [1., 2., 3., 4., 5., 6., 7., 8., 0.],
           [1., 2., 3., 4., 5., 6., 7., 8., 9.]])
    >>> resamples.shape
    (10, 9)

    2. Obtain Jackknife estimate for the mean, its bias, its standard error,
    and its 95% confidence interval:

    >>> test_statistic = np.mean
    >>> estimate, bias, stderr, conf_interval = jackknife_stats(
    ...     data, test_statistic, 0.95)
    >>> estimate
    4.5
    >>> bias
    0.0
    >>> stderr  # doctest: +FLOAT_CMP
    0.95742710775633832
    >>> conf_interval
    array([2.62347735,  6.37652265])

    3. Example for two estimates

    >>> test_statistic = lambda x: (np.mean(x), np.var(x))
    >>> estimate, bias, stderr, conf_interval = jackknife_stats(
    ...     data, test_statistic, 0.95)
    >>> estimate
    array([4.5       ,  9.16666667])
    >>> bias
    array([ 0.        , -0.91666667])
    >>> stderr
    array([0.95742711,  2.69124476])
    >>> conf_interval
    array([[ 2.62347735,   3.89192387],
           [ 6.37652265,  14.44140947]])

    IMPORTANT: Note that confidence intervals are given as columns
    """
    # jackknife confidence interval
    if not (0 < confidence_level < 1):
        raise ValueError("confidence level must be in (0, 1).")

    # make sure original data is proper
    n = data.shape[0]
    if n <= 0:
        raise ValueError("data must contain at least one measurement.")

    # Only import scipy if inputs are valid
    from scipy.special import erfinv

    resamples = jackknife_resampling(data)

    stat_data = statistic(data)
    jack_stat = np.apply_along_axis(statistic, 1, resamples)
    mean_jack_stat = np.mean(jack_stat, axis=0)

    # jackknife bias
    bias = (n-1)*(mean_jack_stat - stat_data)

    # jackknife standard error
    std_err = np.sqrt((n-1)*np.mean((jack_stat - mean_jack_stat)*(jack_stat -
                                    mean_jack_stat), axis=0))

    # bias-corrected "jackknifed estimate"
    estimate = stat_data - bias

    z_score = np.sqrt(2.0)*erfinv(confidence_level)
    conf_interval = estimate + z_score*np.array((-std_err, std_err))

    return estimate, bias, std_err, conf_interval
