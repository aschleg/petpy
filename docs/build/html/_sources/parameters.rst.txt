
.. |organization_id| replace:: Returns results for specified :code:`organization_id`. Can be a str or a tuple or list of str representing multiple organizations.
.. |location| replace:: Returns results by specified location. Must be in the format 'city, state' for city-level results, 'latitude, longitude' for lat-long results, or 'postal code'.
.. |state| replace:: Filters the results by the selected state. Must be a two-letter state code abbreviation of the state name, such as 'WA' for Washington or 'NY' for New York.
.. |country| replace:: Filters results to specified country. Must be a two-letter abbreviation of the country and is limited to the United States and Canada.
.. |query| replace:: Search matching and partially matching name, city or state.
.. |types| replace:: String representing a single animal type or a list or tuple of a collection of animal types. If not specified, all available breeds for each animal type is returned. The animal type must be of 'dog', 'cat', 'rabbit', 'small-furry', 'horse', 'bird', 'scales-fins-other', 'barnyard'.
.. |breed| replace:: String or tuple or list of strings of desired animal type breed to search. Available animal breeds in the Petfinder database can be found using the :code:`breeds()` method.
.. |size| replace:: String or tuple or list of strings of desired animal sizes to return. The specified size(s) must be one of 'small', 'medium', 'large', or 'xlarge'.
.. |gender| replace:: String or tuple or list of strings representing animal genders to return. Must be of 'male', 'female', or 'unknown'.
.. |age| replace:: String or tuple or list of strings specifying animal age(s) to return from search. Must be of 'baby','young', 'adult', 'senior'.
.. |color| replace:: String representing specified animal 'color' to search. Colors for each available animal type in the Petfinder database can be found using the :code:`animal_types()` method.
.. |coat| replace:: Desired coat(s) to return. Must be of 'short', 'medium', 'long', 'wire', 'hairless', or 'curly'.
.. |status| replace:: Animal status to filter search results. Must be one of 'adoptable', 'adopted', or 'found'.
.. |distance| replace:: Returns results within the distance of the specified location. If not given, defaults to 100 miles. Maximum distance range is 500 miles.
.. |sort| replace:: Sorts by specified attribute. Leading dashes represents a reverse-order sort. Must be one of 'recent', '-recent', 'distance', or '-distance'.
.. |results_per_page| replace:: Number of results to return per page. Defaults to 20 results and cannot exceed 100 results per page.
.. |pages| replace:: The number of pages of results to return. For example, if :code:`pages=4` with the default :code:`count` parameter (25), 100 results would be returned. The paged results are returned as a list.
.. |animal_id| replace:: Integer or list or tuple of integers representing animal IDs obtained from Petfinder. When :code:`animal_id` is specified, the other function parameters are overridden. If :code:`animal_id` is not specified, a search of animals on Petfinder matching given criteria is performed.
.. |return_df| replace:: If True, coerces results returned from the Petfinder API into a pandas DataFrame.
.. |raw_results| replace:: The PetFinder API :code:`breeds` endpoint returns some extraneous data in its result set along with the breed names of the specified animal type(s). If :code:`raw_results` is :code:`False`, the method will return a cleaner JSON object result set with the extraneous data removed. This parameter can be set to :code:`True` for those interested in retrieving the entire result set. If the parameter :code:`return_df` is set to :code:`True`, a pandas :code:`DataFrame` will be returned regardless of the value specified for the :code:`raw_result` parameter.
.. |animal_type| replace:: String representing desired animal type to search. Must be one of 'dog', 'cat', 'rabbit', 'small-furry', 'horse', 'bird', 'scales-fins-other', or 'barnyard'.