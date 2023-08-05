# Changelog

## Version 1.0.7 -- 2020-10-11
* Sample applies now suppress logging in addition to stdout and stderr
* Allow new kwargs `offset` and `origin` for pandas df.resample

## Version 1.0.6 -- 2020-09-19
* Fix warnings introduced in 1.0.5 to appropriate warn when using an apply function

## Version 1.0.5 -- 2020-09-19
* Added warnings/errors for swifter methods which do not exist when using modin dataframes
* Updated Dask Dataframe dependencies to require a more recent version
* Updated examples/speed benchmark notebooks

## Version 1.0.4 -- 2020-09-19
* Broken release

## Version 1.0.3 -- 2020-08-03
* Fixed bug with string, axis=1 applies for pandas dataframes that prevented swifter from leveraging modin for parallelization when returning a series instead of a dataframe

## Version 1.0.2 -- 2020-07-31
* Remove pickle5 hard dependency

## Version 1.0.1 -- 2020-07-27
* Reduce resources consumed by swifter by only importing modin/ray when necessary.
* Added `swifter.register_modin()` function, which gives access to `modin.DataFrame.swifter.apply(...)`, but is only required if modin is imported after swifter. If you import modin before swifter, this is not necessary.

## Version 1.0.0 -- 2020-07-27
Two major enhancements are included in this release, both involving the use of modin in swifter. Special thanks to Devin Petersohn for the collaboration.

1. Enable compatibility with modin dataframes. Compatibility not only allows modin dataframes to work with `df.swifter.apply(...)`, but still attempts to vectorize the operation which can lead to a performance boost.

Example:
```python

import modin.pandas as pd
df = pd.DataFrame(...)
df.swifter.apply(...)
```

2. Significantly speed up swifter axis=1 string applies by using Modin, resolving a long-standing issue for swifter.
* Use Modin for axis=1 string applies, unless allow_dask_on_strings(True) is set. If that flag is set, still use Dask.
* NOTE: this means that allow_dask_on_strings() is no longer required to work with text data using swifter.

## Version 0.305
(1) Remove Numba hard dependency, but still handle TypingErrors when numba is installed
(2) Only call tqdm's `progress_apply` on transformations (e.g. Resampler, Rolling) when tqdm has an implementation for that object.

## Version 0.304
Swifter performance consistency improved in two ways:


(1) The validation check of the vectorized form of swifter was always failing, because of assumption of dataframe type, when usually a vectorized function form results in array type.


(2) When using a dataframe with duplicated indices, swifter was silently failing to leverage dask. Now swifter raises a warning when the dataframe has duplicated indices, with a recommendation to call `df.reset_index(drop=True)`.

## Version 0.301
Following pandas release v1.0.0, removing deprecated keyword args "broadcast" and "reduce"

## Version 0.300
Added new `applymap` method for pandas dataframes. `df.swifter.applymap(...)`

## Version 0.297
Fixed issue causing errors when using swifter on empty dataframes. Now swifter will perform a pandas apply on empty dataframes.

## Version 0.296
Added support for resample objects in syntax that refects pandas. `df.swifter.resample(...).apply(...)`

## Version 0.295
Context Manager to suppress print statements during the sample/test applies. Now if a print is part of the function that is applied, the only print that will occur is the final apply's print.

## Version 0.294
Made several code simplifications, thanks to @ianozvsald's suggestions. One of these code changes avoids the issue where assertions are ignored according to python -O flag, which would effectively break swifter.

## Version 0.293
Require tqdm>=4.33.0, which resolves a bug with the progress bar that stems from pandas itself.

## Version 0.292
Fix known security vulnerability in parso <= 0.4.0 by requiring parso > 0.4.0

## Version 0.291
Change import from tqdm.auto instead of tqdm.autenook. Less warnings will show when importing swifter.

## Version 0.290
df.swifter.progress_bar(desc="<Your description>") now allows for a custom description.

## Versions 0.288 and 0.289
Very minor bug fixes for edge cases, e.g. KeyError for applying on a dataframe with a dictionary as a nested element

## Version 0.287
Fixed bugs with rolling apply. Added unit test coverage.

## Version 0.286
Fixed a bug that prevented result_type kwarg from being passed to the dask apply function. Now you can use this functionality and it will rely on dask rather than pandas.

Additionally adjusted the speed estimation for data sets < 25000 rows so that it doesn't spend a lot of time estimating how long to run an apply for on the first 1000 rows when the data set is tiny. We want to asymptote to near-pandas performance even on tiny data sets.

## Version 0.285
Uses tqdm.autonotebook to dynamically switch between beautiful notebook progress bar and CLI version of the progress bar

## Version 0.284
Minor ipywidgets requirements update

## Version 0.283
Allowed user to override scheduler default to multithreading if desired.

## Version 0.282
Add an option `allow_dask_on_strings` to `DataFrameAccessor`. This is a non-recommended option if you are doing string processing. It is intended for using the string as a lookup for the rest of the dataframe processing. This override is also included in `SeriesAccessor`, but there I am not aware of a use-case that it makes sense to use this.

## Version 0.280
Swifter now defaults to axis=0, with a NotImplementedError for when trying to use dask on large datasets, because dask hasn't implemented axis=0 applies yet.

## Version 0.270
Added documentation and code styling thanks to @msampathkumar. Also included override options for dask_threshold and npartitions parameters.

## Version 0.260
Added support for rolling objects in syntax that reflects pandas. `df.swifter.rolling(..).apply(...)`

## Version 0.250
Fixed a bug that would call a vectorized function when in fact the vectorization was wrong to apply. We have to ensure that output data shape is aligned regardless of apply type.

## Version 0.240
Added TQDM support (to disable do `df.swifter.progress_bar(False).apply(...)`, removed groupby_apply (because it's too slow), and tweaked some under-the-hood _dask_apply functionality. Specific functionality changes for pd.Series.swifter.apply include falling back to dask apply if dask map_partitions fails. Specific functionality changes for pd.DataFrame.swifter.apply include falling back to pandas apply if dask apply fails.

## Version 0.230
Made a change so that swifter uses pandas apply when input is series/dataframe of dtype string. This is a temporary solution to slow dask apply processing of strings.

## Version 0.220
Added a groupby_apply function to utilize dask for groupby apply when its faster. Simply use as **df.swifter.groupby_apply(groupby_col, func)**. I would've extended the Pandas DataFrameGroupBy object, but he hasn't added support for that kind of extension yet. Also, removed the str_object limitation to utilizing dask. Now it will simply determine whether to use dask v pandas based on the dask_threshold (default 1 second).

## Version 0.210
Fixed a bug for row-wise applies. Thanks to @slhck for poining this out.

## Version 0.200
Completely refactored the package as an extension to pandas, rather than an independent function call. This will allow for increased flexibility of the user and simplicity of using swiftapply.
**This new update changed the way to use swiftapply. Now the format is df.swifter.apply(func)**

## Version  0.150
Fixed bug that would allow certain functions to be applied to the entire series/dataframe, rather than to each element. For example, len(x) returned the length of the series, rather than the length of each string within the series. A special thanks to @bharatvem for pointing this out.

## Version 0.140
Added support for vectorized and pandas applies to dataframes.
Converted all string manipulations to pandas apply (unless vectorizable) because dask processes string manipulations slowly.

## Version 0.13
Removed numba jit function, because this was adding to the total runtime. Will do some experiments and consider readding later.

## Version 0.1
Currently works very well with pandas series, needs some work to optimize dask multiprocessing for pandas dataframes. For now, it is probably best to apply to each series independently, rather than multiple columns of a dataframe at once.
