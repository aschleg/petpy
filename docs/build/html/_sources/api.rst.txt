
.. _api:

.. currentmodule:: petpy.api
.. include:: parameters.rst

API Reference
=============

:mod:`Petfinder` -- Petfinder API Wrapper
-----------------------------------------

.. class:: Petfinder([key], [secret])

    The Petfinder class provides the wrapper for the Petfinder API. The API methods are listed below

    :param: key: API key received from Petfinder after creating a developer account.
    :param: secret: Secret key received from Petfinder.

Get Animal Types
----------------

.. method:: Petfinder.animal_types([types=None])

    Returns data on an animal type, or types available from the Petfinder API. This data includes the
    available type's coat names and colors, gender and other specific information relevant to the
    specified type(s). The animal type must be of 'dog', 'cat', 'rabbit', 'small-furry', 'horse', 'bird',
    'scales-fins-other', 'barnyard'.

    :param types: |types|
    :rtype: dict. Dictionary object representing JSON data returned from the Petfinder API.


Get Available Animal Breeds
---------------------------

.. method:: Petfinder.breeds([types], [return_df=False], [raw_results=False])

    Returns breed names of specified animal type, or types.

    :param types: |types|
    :param return_df: |return_df|
    :param raw_results: |raw_results|
    :rtype: dict or pandas DataFrame. If the parameter :code:`return_df` is :code:`False`, a dictionary object
            representing the JSON data returned from the Petfinder API is returned. If :code:`return_df=True`, the
            resulting dictionary is coerced into a pandas DataFrame. Note if :code:`return_df=True`, the parameter
            :code:`raw_results` is overridden.

Find Listed Animals on Petfinder
--------------------------------

.. method:: Petfinder.animals([animal_id=None], [animal_type=None], [breed=None], [size=None], [gender=None], [age=None], [color=None], [coat=None], [status=None], [name=None], [organization_id=None], [location=None], [distance=None], [sort=None], [results_per_page=None], [pages=None], [return_df=False])

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
    :param results_per_page: |results_per_page|
    :param return_df: |return_df|
    :rtype: dict or pandas DataFrame. Dictionary object representing the returned JSON object from the Petfinder API.
            If :code:`return_df=True`, the results are returned as a pandas DataFrame.

Get Animal Welfare Organization Data
------------------------------------

.. method:: Petfinder.organizations([organization_id=None], [name=None], [location=None], [distance=None], [state=None], [country=None], [query=None], [sort=True], [results_per_page=None], [pages=None], [return_df=False])

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


API Exceptions
==============

.. class:: PetfinderError(Exception)

    Base Exception class for Petfinder API Exception definitions.

.. class:: PetfinderInvalidCredentials(PetfinderError)

    Exception for handling invalid API and secret keys passed to the Petfinder class.

.. class:: PetfinderInsufficientAccess(PetfinderError)

    Exception for handling insufficient access errors when working with the Petfinder API. This exception is typically
    raised when the credentials supplied to the Petfinder API have expired and the connection to the API needs to be
    re-authenticated.

.. class:: PetfinderResourceNotFound(PetfinderError)

    Exception for handling unknown resource requests.

.. class:: PetfinderUnexpectedError(PetfinderError)

    Exception for handling unexpected errors from the Petfinder API. This error is generally the result of an unknown
    and unexpected error that occurs on the server-side of the Petfinder API when sending a request.

.. class:: PetfinderInvalidParameters(PetfinderError)

    Exception for handling invalid values passed to Petfinder API method parameters.