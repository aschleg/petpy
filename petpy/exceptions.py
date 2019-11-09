class PetfinderError(Exception):
    r"""
    Base Exception class for Petfinder API Exception definitions.

    """
    pass


class PetfinderInvalidCredentials(PetfinderError):
    r"""
    Exception for handling invalid API and secret keys passed to the Petfinder class.

    Parameters
    ----------
    message : str
        Error specifying invalid credentials have been passed to the Petfinder API when initializing the
        Petfinder class
    err : tuple
        Tuple containing the reason for the error and the associated status code.

    Attributes
    ----------
    message : str
        Error specifying invalid credentials have been passed to the Petfinder API when initializing the
        Petfinder class
    err : tuple
        Tuple containing the reason for the error and the associated status code.

    Notes
    -----
    The requests library is used to pass the error reason and status code.

    """
    def __init__(self, message, err, *args):
        self.message = message
        self.err = err

        super(PetfinderInvalidCredentials, self).__init__(message, err, *args)


class PetfinderInsufficientAccess(PetfinderError):
    r"""
    Exception for handling insufficient access errors when working with the Petfinder API. This exception is typically
    raised when the credentials supplied to the Petfinder API have expired and the connection to the API needs to be
    re-authenticated.

    Parameters
    ----------
    message : str
        Error specifying the current credentials supplied to the Petfinder API are insufficient and cannot access the
        requested resource.
    err : tuple
        Tuple containing the reason for the error and the associated status code.

    Attributes
    ----------
    message : str
        Error specifying the current credentials supplied to the Petfinder API are insufficient and cannot access the
        requested resource.
    err : tuple
        Tuple containing the reason for the error and the associated status code.

    Notes
    -----
    The requests library is used to pass the error reason and status code.

    """
    def __init__(self, message, err, *args):
        self.message = message
        self.err = err

        super(PetfinderInsufficientAccess, self).__init__(message, err, *args)


class PetfinderResourceNotFound(PetfinderError):
    r"""
    Exception for handling unknown resource requests.

    Parameters
    ----------
    message : str
        Error specifying the requested resource cannot be found.
    err : tuple
        Tuple containing the reason for the error and the associated status code.

    Attributes
    ----------
    message : str
        Error specifying the requested resource cannot be found.
    err : tuple
        Tuple containing the reason for the error and the associated status code.

    Notes
    -----
    The requests library is used to pass the error reason and status code.

    """
    def __init__(self, message, err, *args):
        self.message = message
        self.err = err

        super(PetfinderResourceNotFound, self).__init__(message, err, *args)


class PetfinderUnexpectedError(PetfinderError):
    r"""
    Exception for handling unexpected errors from the Petfinder API. This error is generally the result of an unknown
    and unexpected error that occurs on the server-side of the Petfinder API when sending a request.

    Parameters
    ----------
    message : str
        Message stating the Petfinder API encountered an unexpected error.
    err : tuple
        Tuple containing the reason for the error and the associated status code.

    Attributes
    ----------
    message : str
        Message stating the Petfinder API encountered an unexpected error.
    err : tuple
        Tuple containing the reason for the error and the associated status code.

    Notes
    -----
    The requests library is used to pass the error reason and status code.

    """
    def __init__(self, message, err, *args):
        self.message = message
        self.err = err

        super(PetfinderUnexpectedError, self).__init__(message, err, *args)


class PetfinderInvalidParameters(PetfinderError):
    r"""
    Exception for handling invalid values passed to Petfinder API method parameters.

    Parameters
    ----------
    message : str
        Message stating the Petfinder API received invalid parameter values.
    err : tuple
        Tuple containing the reason for the error and the associated status code.

    Attributes
    ----------
    message : str
        Message stating the Petfinder API received invalid parameter values.
    err : dict
        The invalid parameters that were passed and the values are that were not accepted.

    """
    def __init__(self, message, err, *args):
        self.message = message
        self.err = err

        super(PetfinderInvalidParameters, self).__init__(message, err, *args)