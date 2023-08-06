from os import path
from sys import stderr
from sys import _getframe
from inspect import signature
from inspect import getsource
from inspect import isfunction
from typing import Callable, Any, Iterable, Tuple, Union, Sequence, Container

from .exceptions import *
from .classes.basic_test import Test
from .classes.data_file import DataFile
from .classes.basic_suite import TestSuite
from .helpers.others import is_file_exists, fake


def test(*args, enabled: bool = True, name: str = None, description: str = None, data_provider: str = None,
         retries: int = 1, groups: Tuple[str] = None, priority: int = 0, timeout: int = 0,
         only_if: Callable[[], bool] = None):
    """
    The annotation that marks a function in a module as a test, does not work with classes and class methods and with
    functions, that take an argument (except using of data provider).
    :param args: parameters, in which a function may come if the method is marked just with  @test.
    :param enabled: is the flag of the active test, if False then the test does not fall into the run and all its other
    settings are ignored.
    :param name: the name of the test, but if there is no name, then the name is the function name
    :param description: Test description, if None will be taken from function documentation. If there are description
    and documentation, then the parameter has the advantage, to wit this is in use, otherwise, documentation will be
    taken from documentation of the function (Test).
    :param data_provider: is the string name of data provider, which is not need to be in current module with test, the
    main is that it was found during assembling of test entities. If not found, the exception UnknownProviderName will
    be raised.
    :param retries: is the total amount of attempts of run test, this is the number of how many times the test will be
    run again in case of errors. If the test is successful, no more attempts are made, fixtures before and after the
    test are run just 1 time!
    :param groups: is the list of group names, to which the test will be assigned, if it empty, group automatically
    creates with the name of the module. This parameter allows to group tests from different modules to one run.
    :param priority: is the priority, for organization of tests execution order. The greater is 0, as parameter high the
    execution of the test will be done later.
    :param timeout is the number of seconds during waiting the test ends. If the test had not end, then
    TestBrokenException exception will raised, and the thread, in which the test is executing, will be interrupted.
    Due to a possible memory leak, it should be used only when there is a special need.
    :param only_if: accepts a function that will be called before the test starts and the test will only be launched if
    it returns True. Should be taken to filter tests, for instance in relation to the operating system used.
    :return: fake
    """
    if not enabled:
        return fake

    def real_decorator(func: Callable[[], None]):
        if not data_provider:
            __check_is_function_without_args(func, 'test')
        else:
            __check_is_function_for_provider(func)
        name_ = name if name else func.__name__
        _check_func_for_soft_assert(func)
        if only_if is not None and not callable(only_if):
            raise ValueError('Only_if parameter of @test annotation must be a function, returning True or False!')
        nonlocal groups
        if not groups:
            groups = [func.__module__]
        else:
            if type(groups) not in (list, tuple, set):
                raise ValueError('Group parameter of @test annotation must be a tuple of strings (Tuple[str])!')
        for group in groups:
            test_object = Test(name_, func)
            test_object.only_if = only_if
            test_object.retries = retries
            test_object.priority = priority
            if description:
                test_object.description = description
            if timeout:
                test_object.timeout = int(timeout)
                if test_object.timeout < 0:
                    test_object.timeout = 0
            if data_provider:
                test_object.provider = data_provider
            TestSuite.get_instance().get_or_create(group).add_test(test_object)
        return fake

    if args:
        return real_decorator(args[0])
    return real_decorator


def provider(*args, enabled: bool = True, name: str = None, cached: bool = False,
             map_to_str: Callable[[Any], str] = str):
    """
    The annotation that marks a data provider, that is, a function that supplies data to a test. Such a function should
    return Iterable or Sequence, otherwise will be an error. It is not possible at compile time to determine if the
    function returns the correct type, so an exception with the wrong type will be thrown at runtime. Exception tests
    with such provider are added to ignored.
    :param args: are parameters in which a function may come if the method is marked simply with @data
    :param enabled: the flag of the active provider, if False, then it does not fall into the list of providers and all
    its other settings are ignored
    :param name: is the name, if not specified, then takes the name of the function. By this name, tests are searched by
    the provider, therefore only unique names are allowed. Duplicate name throws DuplicateNameException
    :param cached: flag to save all provider data in memory and use it on second use. Can be useful only when provider
    used more than once in test-suite and you do not want to get data again from some source like filesystem or db.
    WARNING! Cache use memory, so it can take a lot of it for big data volumes.
    :param map_to_str: function-mapper to represent item of provider
    :return: fake
    :raise DuplicateProviderNameException if provider with such name is already exists
    :raise WrongDecoratedObject if @data annotation used on function without return or yield statements
    """
    if not enabled:
        return fake

    def real_decorator(func: Callable[[None], Iterable]):
        __check_is_function_without_args(func, 'data')
        if not _has_yield_or_return(func):
            raise WrongDecoratedObject(f'Function marked with @data must returns or yields Iterable!')
        name_ = name if name else func.__name__
        providers = TestSuite.get_instance().providers
        if name_ in providers:
            raise DuplicateProviderNameException(f'Provider with name "{name_}" already exists! '
                                                 f'Only unique names allowed!')
        providers[name_] = (func, map_to_str)
        nonlocal cached
        if cached:
            TestSuite.get_instance().cached.append(name_)
        return fake

    if args:
        return real_decorator(args[0])
    return real_decorator


def before(*args, group_name: str = None):
    """
    It marks the function as mandatory to run before each module/group test.
    :param group_name: the name of the group before which test the function will be executed. If no group name is
    specified, a group is automatically created with the module name. A function does not have to be in the same module
    as the tests.
    :return: fake
    """

    def real_decorator(func: Callable[[], None]):
        __check_is_function_without_args(func, 'before')
        group = group_name if group_name else func.__module__
        TestSuite.get_instance().get_or_create(group).add_before_test(func)
        return fake

    if args:
        return real_decorator(args[0])
    return real_decorator


def after(*args, group_name: str = None):
    """
    It marks the function as mandatory to run after each module/group test. If there are functions running before the
    test (@before) and they failed, then these functions will not start!
    :param group_name: the name of the group after each test of which the function will be executed. If the group name
    is not specified, a group with the module name is automatically created. A function does not have to be in the same
    module as the tests.
    :return: fake
    """

    def real_decorator(func: Callable[[], None]):
        __check_is_function_without_args(func, 'after')
        group = group_name if group_name else func.__module__
        TestSuite.get_instance().get_or_create(group).add_after_test(func)
        return fake

    if args:
        return real_decorator(args[0])
    return real_decorator


def before_group(*args, name: str = None):
    """
    Marks a function as a mandatory part of a test group bootstrap process.
    The marked function is executed once strictly before any of the tests in the specified test group.
    Use this decorator to build test fixtures for individual test groups.

    :param name: the name of a module or a test group the function is executed in advance of,
    if no name is specified, the name of the current module is used
    :return: fake
    """

    def real_decorator(func: Callable[[], None]):
        __check_is_function_without_args(func, 'before_module')
        group = name if name else func.__module__
        TestSuite.get_instance().get_or_create(group).add_before(func)
        return fake

    if args:
        return real_decorator(args[0])
    return real_decorator


def after_group(*args, name: str = None, always_run: bool = False):
    """
    Marks a function as a mandatory part of a test group teardown process.
    The marked function is executed once strictly after all of the tests in a group have finished running.
    The marked function is not executed if @before_group fails, unless always_run set to True.
    Use this decorator to correctly tear down fixtures built for individual test groups.

    :param name: the name of a module or a test group the function is executed after
    if no name is specified, the name of the current module is used
    :param args: handles the call-less @after_group decorator shorthand, holds the wrapped function reference
    :param always_run: if False, execute only if @before_group has finished successfully,
    if True, force the function execution anyway
    :return: fake
    """

    def real_decorator(func: Callable[[], None]):
        __check_is_function_without_args(func, 'after_module')
        group = name if name else func.__module__
        TestSuite.get_instance().get_or_create(group).add_after(func)
        if always_run:
            TestSuite.get_instance().get_or_create(group).always_run_after = True
        return fake

    if args:
        return real_decorator(args[0])
    return real_decorator


def before_suite(func: Callable[[], None]):
    """
    Marks a function as a mandatory part of the whole test suite bootstrap process.
    The marked function is executed once strictly before any of the tests and functions, marked with @before_group.
    Use this decorator to build test fixtures for the whole test suite.

    :param func: a callable object, must not take any arguments
    :return: None
    """
    __check_is_function_without_args(func, 'before_suite')
    TestSuite.get_instance().add_before(func)


def after_suite(*args, always_run: bool = False):
    """
    Marks a function as a mandatory part of a test suite teardown process.
    The marked function is executed once strictly after all of the test in the suite have finished running and
    all of the functions marked with @before_group are executed.
    The marked function is not executed if @before_suite fails, unless always_run set to True.
    Use this decorator to correctly tear down fixtures built for the whole test suite.

    :param args: handles the call-less @after_suite decorator shorthand, holds the wrapped function reference
    :param always_run: if False, execute only if @before_suite has finished successfully,
    if True, force the function execution anyway
    :return: fake
    """

    def real_decorator(func: Callable[[], None]):
        __check_is_function_without_args(func, 'after_suite')
        TestSuite.get_instance().add_after(func)
        if always_run:
            TestSuite.always_run_after = True
        return fake

    if args:
        return real_decorator(args[0])
    return real_decorator


def _has_yield_or_return(function: Callable) -> bool:
    code = getsource(function)
    return ' return ' in code or ' yield ' in code


def _check_func_for_soft_assert(func):
    try:
        code = getsource(func)
        is_soft_assert_there = 'SoftAssert(' in code
        if not is_soft_assert_there:
            return
        if 'assert_all()' not in code:
            print(f'WARNING! Function {func.__module__}.{func.__name__} marked with @test seems to contains SoftAssert '
                  f'object without calling assert_all()!', file=stderr)
    except Exception:
        # Consciously ignore it, just check for a warning, this is not critical
        pass


def __check_is_function_without_args(func: Callable, annotation_name: str):
    """
    Checking that the annotation is above the function without arguments, it is not intended to use annotations with
    classes and / or with their methods.
    :param func: is the function to test
    :param annotation_name: is the name of annotation (for errors)
    :return: None
    :raise: WrongAnnotationPlacement
    """
    if not isfunction(func) or signature(func).parameters:
        raise WrongDecoratedObject(
            f"Annotation '{annotation_name}' must be used only with no-argument functions! Its not supposed to work "
            f"with classes or class methods!")


def __check_is_function_for_provider(func: Callable[[Any], None]):
    """
    Check that the function is suitable to accept values (use a data provider), that is, it has exactly 1 argument.
    :param func: is the function
    :return: None
    :raise WrongDecoratedObject
    """
    if not isfunction(func) or not signature(func).parameters:
        raise WrongDecoratedObject(f"Function '{func.__name__}' marked with data_provider has no argument!")
    if len(signature(func).parameters) > 1:
        raise WrongDecoratedObject(f"Function '{func.__name__}' marked with data_provider "
                                   f"has more than 1 argument!")


def DATA_FILE(file_path: str, name: str = None, cached: bool = False, encoding: str = 'UTF-8',
              map_function: Callable = None):
    """
    Function to use text file as data provider for test. Reads file lazily, do not get it to memory.
    The function name explicitly stays uppercase for user to pay attention to it.
    User must call it at the global module namespace, but not at fixtures or in tests!
    :param name: name of the data-provider for use it in test, if not specified the file_path be used as name
    :param cached: flag to cache values for using it more than once
    :param file_path: file name or path-to-file with name, it can be full or relative path, but it must be "visible"
    (accessible from module, where it is declared)
    :param encoding: encoding of the text file (default UTF-8)
    :param map_function: function, which map line from text file
    :return: None
    :raise FileNotFoundError if file is not exists!
    """

    def wrapper():
        return DataFile(real_path, encoding=encoding, map_function=map_function)

    if name is None:
        name = file_path
    try:
        # Get last frame to verify file-path
        frame = _getframe(1)
        assert frame  # It can't be no last frame!
        first_path = path.split(frame.f_globals['__file__'])[0]
        real_path = path.join(first_path, file_path)
        if not is_file_exists(real_path):
            raise FileNotFoundError(f'Cant find file! Is file "{real_path}" exists?')
        provider(name=name, cached=cached)(wrapper)
    finally:
        del frame


def CONTAINER(value: Union[Sequence, Iterable, Container], name: str = None, map_to_str: Callable[[Any], str] = str):
    """
    Sugar for simplify providing data, use it when provider is simple and can be written in one-liner, like list
    comprehension or generator expression.
    The function name explicitly stays uppercase for user to pay attention to it!
    User must call it at the global module namespace, but not at fixtures or in tests!
    :param value: sequence/iterable or any object you can use with for
    :param name: name for the provider, if empty then 'container' will be used as name
    :param map_to_str: function-mapper to represent item of provider
    :return: None
    """

    def _():
        return value

    name = name if name is not None else 'container'
    provider(name=name, map_to_str=map_to_str)(_)
