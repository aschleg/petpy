.. _API_parameters:

.. |animal| replace:: Return breeds of animal. Must be one of 'barnyard', 'bird', 'cat', 'dog', 'horse', 'reptile', or 'smallfurry'.
.. |outputformat| replace:: Output type of results. Must be one of 'json' (default) or 'xml'.
.. |location| replace:: ZIP/postal code, state, or city and state to perform the search.
.. |breed| replace:: Specifies the breed of the animal to search.
.. |size| replace:: Specifies the size of the animal/breed to search. Must be one of 'S' (small), 'M' (medium), 'L' (large), 'XL' (extra-large).
.. |sex| replace:: Filters the search to the desired gender of the animal. Must be one of 'M' (male) or 'F' (female).
.. |age| replace:: Returns animals with specified age. Must be one of 'Baby', 'Young', 'Adult', 'Senior'.
.. |offset| replace:: Can be set to the value of :code:`lastOffset` returned from the previous call to retrieve the next set of results. The :code:`pages` parameter can also be used to pull a desired number of paged results.
.. |count| replace:: The number of records to return. Default is 25.
.. |pages| replace:: The number of pages of results to return. For example, if :code:`pages=4` with the default :code:`count` parameter (25), 100 results would be returned. The paged results are returned as a list.
.. |records| replace:: Returns :code:`records` random results. Each returned record is counted as one call to the Petfinder API.
.. |output| replace:: Sets the amount of information returned in each record. 'basic' returns a simple record while 'full' returns a complete record with description. Defaults to 'basic'.
.. |petId| replace:: ID of the pet record to return.
.. |shelterId| replace:: Filter results to a specific shelter.
.. |return_df| replace:: If True, coerces results returned from the Petfinder API into a pandas DataFrame.
.. |status| replace:: Filters search by pet's status. Must be one of 'A' (adoptable, default), 'H' (hold), 'P' (pending), 'X' (adopted/removed).
.. |name| replace:: Full or partial shelter name