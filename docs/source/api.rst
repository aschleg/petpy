

.. _api:

.. currentmodule:: petpy.api
.. include:: parameters.rst

API Reference
=============

:mod:`Petfinder` -- Petfinder API Wrapper
-----------------------------------------

.. class:: Petfinder([key], [secret=None], [host='http://api.petfinder.com/'])

    The Petfinder class provides the wrapper for the Petfinder API. The API methods are listed below

Pet Methods
-----------

.. method:: Petfinder.breed_list([animal], [outputformat='json'], [return_df=False])

    Method for calling the 'breed.list' method of the Petfinder API. Returns the available breeds
    for the selected animal.

    :param animal: |animal|
    :param outputformat: |outputformat|
    :param return_df: |return_df|
    :rtype: json, str. or pandas DataFrame If the parameter :code:`outputformat` is 'json',
        the result is formatted as a JSON object. Otherwise, the return object is a text
        representation of an XML object. If :code:`return_df` is :code:`True`, :code:`outputformat`
        is overridden and the results are converted to a pandas DataFrame. Please note there may
        be some loss of data when the conversion is made; however, this loss is primarily confined
        to the call encoding and timestamp information and metadata of the associated media (photos)
        with a record.

.. method:: Petfinder.pet_find([location], [animal=None], [breed=None], [size=None], [sex=None], [age=None], [offset=None], [count=None], [pages=None], [output=None], [outputformat='json'], [return_df=False)

    Returns a collection of pet records matching input parameters. Wrapper for 'pet.find' method in the Petfinder API.

    :param location: |location|
    :param animal: |animal|
    :param breed: |breed|
    :param size: |size|
    :param sex: |sex|
    :param age: |age|
    :param offset: |offset|
    :param count: |count|
    :param pages: |pages|
    :param output: |output|
    :param outputformat: |outputformat|
    :param return_df: |return_df|
    :rtype: json, list of json, str, list of str or pandas DataFrame. Pet records matching the desired search parameters.
            If the parameter :code:`outputformat` is 'json', the result is formatted as a JSON object.
            Otherwise, the return object is a text representation of an XML object. If the :code:`pages`
            parameter is set, the paged results are returned as a list. If :code:`return_df` is :code:`True`,
            :code:`outputformat` is overridden and the results are converted to a pandas DataFrame. Please
            note there may be some loss of data when the conversion is made; however, this loss is primarily
            confined to the call encoding and timestamp information and metadata of the associated media (photos)
            with a record.

.. method:: Petfinder.pet_get([petId], [outputformat='json'], [return_df=False])

    Returns a single record for a pet. Wrapper for 'pet.get' method in the Petfinder API.

    :param petId: |petId|
    :param outputformat: |outputformat|
    :param return_df: |return_df|
    :rtype: json, str or pandas DataFrame. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object. If :code:`return_df` is :code:`True`, :code:`outputformat`
            is overridden and the results are converted to a pandas DataFrame. Please note there may
            be some loss of data when the conversion is made; however, this loss is primarily confined
            to the call encoding and timestamp information and metadata of the associated media (photos)
            with a record.

.. method:: Petfinder.pets_get([petId], [outputformat='json'], [return_df=False])

    Convenience wrapper of :code:`pet_get` for returning multiple pet records given a list or tuple of pet IDs.

    :param petId: list or tuple containing pet IDs to search.
    :param outputformat: |outputformat|
    :param return_df: |return_df|
    :rtype: list or pandas DataFrame. Matching record corresponding to input pet ID. If the parameter
            :code:`outputformat` is 'json', the result is formatted as a JSON object. Otherwise,
            the return object is a text representation of an XML object. If :code:`return_df`
            is :code:`True`, :code:`outputformat` is overridden and the results are converted to a
            pandas DataFrame. Please note there may be some loss of data when the conversion is made;
            however, this loss is primarily confined to the call encoding and timestamp information and
            metadata of the associated media (photos) with a record.

.. method:: Petfinder.pet_getRandom([animal=None], [breed=None], [size=None], [sex=None], [location=None], [shelterId=None], [records=None], [output=None], [outputformat='json'], [return_df=False])

    Returns a randomly selected pet record. The possible result can be filtered with input parameters.
    Wrapper for 'pet.getRandom' method in the Petfinder API.

    :param animal: |animal|
    :param breed: |breed|
    :param size: |size|
    :param sex: |sex|
    :param location: |location|
    :param shelterId: |shelterId|
    :param output: |output|
    :param records: |records|
    :param outputformat: |outputformat|
    :param return_df: |return_df|
    :rtype: json, str or pandas DataFrame. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object. If :code:`records` is specified, a list of the results
            is returned. If :code:`return_df` is :code:`True`, :code:`outputformat` is overridden and
            the results are converted to a pandas DataFrame. Please note there may be some loss of data
            when the conversion is made; however, this loss is primarily confined to the call encoding
            and timestamp information and metadata of the associated media (photos) with a record.

Shelter Methods
---------------

.. method:: Petfinder.shelter_find([location], [name=None], [offset=None], [count=None], [pages=None], [outputformat='json'], [return_df=False])

    Returns a collection of shelter records matching input parameters. Wrapper for the 'shelter.find' method
    in the Petfinder API.

    :param location: |location|
    :param name: |name|
    :param offset: |offset|
    :param count: |count|
    :param pages: |pages|
    :param outputformat: |outputformat|
    :param return_df: |return_df|
    :rtype: json, list of json, str, list of str or pandas DataFrame. Shelters matching specified input parameters.
            If the parameter :code:`outputformat` is 'json', the result is formatted as a JSON
            object. Otherwise, the return object is a text representation of an XML object. If
            the :code:`pages` parameter is set, the paged results are returned as a list. If :code:`return_df`
            is :code:`True`, :code:`outputformat` is overridden and the results are converted to a pandas
            DataFrame. Please note there may be some loss of data when the conversion is made; however,
            this loss is primarily confined to the call encoding and timestamp information and metadata
            of the associated media (photos) with a record.

.. method:: Petfinder.shelter_get([shelterId], [outputformat='json'], [return_df=False])

    Returns a single shelter record. Wrapper for the 'shelter.get' method in the Petfinder API.

    :param shelterId: |shelterId|
    :param outputformat: |outputformat|
    :param return_df: |return_df|
    :rtype: json, str or pandas DataFrame. If the parameter :code:`outputformat` is 'json',
            the result is formatted as a JSON object. Otherwise, the return object is a text
            representation of an XML object. If :code:`return_df` is :code:`True`, :code:`outputformat`
            is overridden and the results are converted to a pandas DataFrame. Please note there may
            be some loss of data when the conversion is made; however, this loss is primarily confined
            to the call encoding and timestamp information and metadata of the associated media (photos)
            with a record.

.. method:: Petfinder.shelters_get([shelterId], [outputformat='json'], [return_df=False])

    Returns multiple shelter records given a list or tuple of shelter IDs. Convenience wrapper function of :code:`shelter_get()`.

    :param shelterId: list or tuple containing shelter IDs to search.
    :param outputformat: |outputformat|
    :param return_df: |return_df|
    :rtype: list or pandas DataFrame. Shelter record of input shelter ID. If the parameter
            :code:`outputformat` is 'json', the result is formatted as a JSON object. Otherwise,
            the return object is a text representation of an XML object. If :code:`return_df` is
            :code:`True`, :code:`outputformat` is overridden and the results are converted to a
            pandas DataFrame. Please note there may be some loss of data when the conversion is made;
            however, this loss is primarily confined to the call encoding and timestamp information
            and metadata of the associated media (photos) with a record.

.. method:: Petfinder.shelter_getPets([shelterId], [status=None], [offset=None], [count=None], [output=None], [pages=None], [outputformat='json'], [return_df=False])

    Returns a collection of pet records for an individual shelter. Wrapper for the 'shelter_getPets' method
    in the Petfinder API.

    :param shelterId: |shelterId|
    :param status: |status|
    :param offset: |offset|
    :param count: |count|
    :param pages: |pages|
    :param output: |output|
    :param outputformat: |outputformat|
    :param return_df: |return_df|
    :rtype: json, list of json, str, list of str or pandas DataFrame.
            Pet records of given shelter matching optional input parameters. If the parameter
            :code:`outputformat` is 'json', the result is formatted as a JSON object. Otherwise, the return
            object is a text representation of an XML object. If the :code:`pages` parameter is set, the
            paged results are returned as a list. If :code:`return_df` is :code:`True`, :code:`outputformat`
            is overridden and the results are converted to a pandas DataFrame. Please note there may
            be some loss of data when the conversion is made; however, this loss is primarily confined
            to the call encoding and timestamp information and metadata of the associated media (photos)
            with a record.

.. method:: Petfinder.shelter_listByBreed([animal], [breed], [offset=None], [count=None], [pages=None], [outputformat='json'], [return_df=False])

    Returns a list of shelter IDs listing animals matching the input animal breed. Wrapper for the
    'shelter.listByBreed' method in the Petfinder API.

    :param animal: |animal|
    :param breed: |breed|
    :param offset: |offset|
    :param count: |count|
    :param pages: |pages|
    :param outputformat: |outputformat|
    :param return_df: |return_df|
    :rtype: json, list of json, str or list of str. Shelter IDs listing animals matching the input
            animal breed. If the parameter :code:`outputformat` is 'json', the result is formatted
            as a JSON object. Otherwise, the return object is a text representation of an XML object.
            If the :code:`pages` parameter is set, the paged results are returned as a list. If :code:`return_df`
            is :code:`True`, :code:`outputformat` is overridden and the results are converted to a pandas
            DataFrame. Please note there may be some loss of data when the conversion is made; however,
            this loss is primarily confined to the call encoding and timestamp information and metadata
            of the associated media (photos) with a record.