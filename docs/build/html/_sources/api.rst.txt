
.. _api:

.. currentmodule:: petpy.api
.. include:: parameters.rst

API Reference
=============

:mod:`Petfinder` -- Petfinder API Wrapper
-----------------------------------------

.. class:: Petfinder(key, secret)

    The Petfinder class provides the wrapper for the Petfinder API. The API methods are listed below

    :param key: API key received from Petfinder after creating a developer account.
    :param secret: Secret key received from Petfinder.

    .. code-block:: python

        import petpy
        pf = Petfinder(key=API_key, secret=API_secret)

Get Animal Types
----------------

.. method:: Petfinder.animal_types([types=None])

    Returns data on an animal type, or types available from the Petfinder API. This data includes the
    available type's coat names and colors, gender and other specific information relevant to the
    specified type(s). The animal type must be of 'dog', 'cat', 'rabbit', 'small-furry', 'horse', 'bird',
    'scales-fins-other', 'barnyard'.

    :param types: |types|
    :rtype: dict. Dictionary object representing JSON data returned from the Petfinder API.

    .. code-block:: python

       # All animal types and their relevant data.
       all_types = pf.animal_types()

       # Returning data for a single animal type
       dogs = pf.animal_types('dog')

       # Getting multiple animal types at once
       cat_dog_rabbit_types = pf.animal_types(['cat', 'dog', 'rabbit'])

Get Available Animal Breeds
---------------------------

.. method:: Petfinder.breeds(types[, return_df=False][, raw_results=False])

    Returns breed names of specified animal type, or types.

    :param types: |types|
    :param return_df: |return_df|
    :param raw_results: |raw_results|
    :rtype: dict or pandas DataFrame. If the parameter :code:`return_df` is :code:`False`, a dictionary object
            representing the JSON data returned from the Petfinder API is returned. If :code:`return_df=True`, the
            resulting dictionary is coerced into a pandas DataFrame. Note if :code:`return_df=True`, the parameter
            :code:`raw_results` is overridden.

    .. code-block:: python

           cat_breeds = pf.breeds('cat')
           dog_breeds = pf.breeds('dog')

           # All available breeds or multiple breeds can also be returned.
           all_breeds = pf.breeds()
           cat_dog_rabbit = pf.breeds(types=['cat', 'dog', 'rabbit'])

           # The `breeds` method can also be set to coerce the returned JSON results into a pandas DataFrame
           # by setting the parameter `return_df = True`.

           cat_breeds_df = pf.breeds('cat', return_df = True)
           all_breeds_df = pf.breeds(return_df = True)

Find Listed Animals on Petfinder
--------------------------------

.. method:: Petfinder.animals([animal_id=None][, animal_type=None][, breed=None][, size=None][, gender=None][, age=None][, color=None][, coat=None][, status=None][, name=None][, organization_id=None][, location=None][, distance=None][, sort=None][, results_per_page=None][, pages=None][, return_df=False])

    Returns adoptable animal data from Petfinder based on specified criteria.

    :param animal_id: |animal_id|
    :param animal_type: |animal_type|
    :param breed: |breed|
    :param size: |size|
    :param gender: |gender|
    :param age: |age|
    :param color: |color|
    :param coat: |coat|
    :param status: |status|
    :param name: Searches for animal names matching or partially matching name.
    :param organization_id: |organization_id|
    :param location: |location|
    :param distance: |distance|
    :param sort: |sort|
    :param pages: |pages|
    :param good_with_cats: Filters returned animal results to animals that are designated as good with cats. Must be a boolean value
                           (True, False) or a value that can be coerced to a boolean (1, 0).
    :param good_with_children: Filters returned animal results to animals that are designated as good with children. Must be a boolean value
                               (True, False) or a value that can be coerced to a boolean (1, 0).
    :param good_with_dogs: Filters returned animal results to animals that are designated as good with dogs. Must be a boolean value
                           (True, False) or a value that can be coerced to a boolean (1, 0).
    :param before_date: Returns results with a `published_at` datetime before the specified time. Must be a string in the form of
                        'YYYY-MM-DD' or 'YYYY-MM-DD H:M:S' or a datetime object.
    :param after_date: Returns results with a `published_at` datetime after the specified time. Must be a string in the form of
                       'YYYY-MM-DD' or 'YYYY-MM-DD H:M:S' or a datetime object.
    :param results_per_page: |results_per_page|
    :param return_df: |return_df|
    :rtype: dict or pandas DataFrame. Dictionary object representing the returned JSON object from the Petfinder API.
            If :code:`return_df=True`, the results are returned as a pandas DataFrame.

    .. code-block:: python

        # Getting first 20 results without any search criteria
        animals = pf.animals()

        # Extracting data on specific animals with animal_ids

        animal_ids = []
        for i in animals['animals'][0:3]:
           animal_ids.append(i['id'])

        animal_data = pf.animals(animal_id=animal_ids)

        # Returning a pandas DataFrame of the first 150 animal results
        animals = pf.animals(results_per_page=50, pages=3, return_df=True)

Get Animal Welfare Organization Data
------------------------------------

.. method:: Petfinder.organizations([organization_id=None][, name=None][, location=None][, distance=None][, state=None][, country=None][, query=None][, sort=True][, results_per_page=None][, pages=None][, return_df=False])

    Returns data on an animal welfare organization, or organizations, based on specified criteria.

    :param organization_id: |organization_id|
    :param name: Returns results matching or partially matching organization name.
    :param location: |location|
    :param distance: |distance|
    :param state: |state|
    :param country: |country|
    :param query: |query|
    :param sort: |sort|
    :param count: |results_per_page|
    :param pages: |pages|
    :param return_df: |return_df|
    :rtype: dict or pandas DataFrame. Dictionary object representing the returned JSON object from the Petfinder API.
            If :code:`return_df=True`, the results are returned as a pandas DataFrame.

    .. code-block:: python

        # Return the first 1,000 animal welfare organizations as a pandas DataFrame
        organizations = pf.organizations(results_per_page=100, pages=10, return_df=True)

        # Get organizations in the state of Washington
        wa_organizations = pf.organizations(state='WA')
