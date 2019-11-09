
.. _exceptions:

.. currentmodule:: petpy.exceptions


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
