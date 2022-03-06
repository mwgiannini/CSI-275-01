"""Test classes for Lab/HW 3.

Champlain College CSI-235, Spring 2019
The following code was adapted by Joshua Auerbach (jauerbach@champlain.edu)
from the UC Berkeley Pacman Projects (see license and attribution below).

----------------------
Licensing Information:  You are free to use or extend these projects for
educational purposes provided that (1) you do not distribute or publish
solutions, (2) you retain this notice, and (3) you provide clear
attribution to UC Berkeley, including a link to http://ai.berkeley.edu.

Attribution Information: The Pacman AI projects were developed at UC Berkeley.
The core projects and autograders were primarily created by John DeNero
(denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
Student side autograding was added by Brad Miller, Nick Hay, and
Pieter Abbeel (pabbeel@cs.berkeley.edu).
"""

import test_classes
import socket
import os
from struct import Struct

from constants import (HOST, UPLOAD_PORT, FIXED_LENGTH_TEST_PORT,
                       DELIMITER_TEST_PORT, BAD_PORT)


class Lab3Test(test_classes.TestCase):
    """Base class for Lab3 tests."""

    def __init__(self, question, test_dict):
        """Extend test_classes.TestCase.__init__."""
        super().__init__(question, test_dict)
        self.good_files = ["test_files/good_file1.dat",
                           "test_files/good_file2.dat"]  # ,"upload_client.py"]
        self.bad_files = ["test_files/bad_file.dat"]

    def write_solution(self, module_dict, file_path):
        """Write solution for the test.

        Overrides test_classes.TestCase.write_solution to write a blank
        solution.
        """
        handle = open(file_path, 'w')
        handle.write('# This is the solution file for %s.\n' % self.path)
        handle.write('# This file is left blank intentionally.\n')
        handle.close()
        return True

    def add_pass_message(self, grades):
        """Add a passing message to grades."""
        grades.add_message('PASS: {}'.format(self.path))

    def add_fail_messages(self, grades, messages):
        """Add failing messages to grades."""
        grades.add_message('FAIL: {}'.format(self.path))
        for message in messages:
            grades.add_message('\t' + message)

    def get_socket(self, client, include_key=False):
        """Get socket member variable from client object.

        If include_key set to True, return will be a tuple(key, value)
        where key is the name of the socket instance and value is the socket
        instance itself.
        """
        for key, value in client.__dict__.items():
            if(isinstance(value, socket.socket)):
                if include_key:
                    return key, value
                return value


class BasicUploadClientTest(Lab3Test):
    """Test case for question 1."""

    def execute(self, grades, module_dict, solution_dict):
        """Run student code.

        Overrides test_classes.TestCase.execute
        """
        upload_client = module_dict["upload_client"]
        passing_all = True

        # test timeout
        grades.add_message("Testing bad connection...")
        try:
            client = upload_client.UploadClient(HOST, BAD_PORT)
        except (ConnectionError, TimeoutError):
            self.add_pass_message(grades)
        else:
            self.add_fail_messages(grades,
                                   ["Did not timeout on initialization"
                                    " when connecting to invalid port"])
            passing_all = False

        # test connecting to upload server
        sock = None
        grades.add_message("Testing initialization...")
        try:
            client = upload_client.UploadClient(HOST, UPLOAD_PORT)
        except (ConnectionError, TimeoutError):
            self.add_fail_messages(grades, ["Connection error when connecting "
                                            "to valid port, check internet "
                                            "connection"])
            passing_all = False
        else:
            try:
                key, sock = self.get_socket(client, True)
            except TypeError:
                sock = None
            if sock:
                grades.add_message(f"Found socket member variable {key}.")
                if sock.type != socket.SOCK_STREAM:
                    self.add_fail_messages(grades,
                                           ["Socket is of wrong type"])
                    passing_all = False

                elif sock.family != socket.AF_INET:
                    self.add_fail_messages(grades,
                                           ["Socket is of wrong family"])
                    passing_all = False

                else:
                    try:
                        sock.getpeername()
                        self.add_pass_message(grades)
                    except OSError:
                        self.add_fail_messages(grades,
                                               ["Socket is not connected"])
                        passing_all = False

        if not sock:
            self.add_fail_messages(grades,
                                   ["No socket member variable found."])
            passing_all = False

        else:
            grades.add_message("Testing closing...")
            client.close()
            try:
                sock.getpeername()
            except OSError:
                self.add_pass_message(grades)
            else:
                self.add_fail_messages(grades,
                                       ["Socket did not close properly"])
                passing_all = False

        return passing_all


class RecvAllTest(Lab3Test):
    """Test case for Question 2."""

    def execute(self, grades, module_dict, solution_dict):
        """Run student code.

        Overrides test_classes.TestCase.execute
        """
        upload_client = module_dict["upload_client"]
        passing_all = True

        client = upload_client.UploadClient(HOST, FIXED_LENGTH_TEST_PORT)
        sock = self.get_socket(client)

        size_struct = Struct("!I")

        for size in [1, 1024, 4096]:
            expected_result = b"FIXED_LENGTH" * size

            grades.add_message(f"Testing recv_all {len(expected_result)}...")
            sock.sendall(size_struct.pack(size))

            result = client.recv_all(len(expected_result))
            if expected_result == result:
                self.add_pass_message(grades)
            else:
                self.add_fail_messages(
                    grades, ["Did not receive expected response from recv_all"]
                    )
                passing_all = False

        client.close()
        return passing_all


class RecvUntilDelimiterTest(Lab3Test):
    """Test case for Question 3."""

    def execute(self, grades, module_dict, solution_dict):
        """Run student code.

        Overrides test_classes.TestCase.execute
        """
        upload_client = module_dict["upload_client"]
        passing_all = True

        client = upload_client.UploadClient(HOST, DELIMITER_TEST_PORT)
        sock = self.get_socket(client)

        grades.add_message("Testing recv_until_delimiter (single)...")
        sock.sendall(b"%")
        result = client.recv_until_delimiter(b"%")
        expected_result = b"DELIMITER" * 4096

        if result == expected_result:
            self.add_pass_message(grades)
        else:
            self.add_fail_messages(
                grades,
                ["Did not receive expected response from recv_until_delimiter"]
                )
            passing_all = False

        grades.add_message("Testing recv_until_delimiter (multiple)...")
        sock.sendall(b"\n")

        for i in range(10):
            result = client.recv_until_delimiter(b"\n")
            expected_result = b"NEW LINES" * 16 * (i+1)
            if result != expected_result:
                self.add_fail_messages(grades,
                                       ["Did not receive expected response "
                                        "from recv_until_delimiter"])
                passing_all = False
                break
        else:
            self.add_pass_message(grades)

        client.close()
        return passing_all


class UploadTest(Lab3Test):
    """Test case for Question 4."""

    def _execute_helper(self, grades, client, ex):
        passing_all = True

        for path in self.good_files:
            grades.add_message("Testing uploading " + path + "...")
            try:
                client.upload_file(path)
            except ex:
                self.add_fail_messages(grades, ["Error on uploading " + path])
                passing_all = False
            else:
                self.add_pass_message(grades)

        # Commented out by JOR 2/23/2020 because I couldn't
        # figure out what the heck was wrong with the file

        # for path in self.bad_files:
        #     grades.add_message("Testing uploading " + path + "...")
        #     try:
        #         client.upload_file(path)
        #     except ex:
        #         self.add_pass_message(grades)
        #     else:
        #         self.add_fail_messages(grades,
        #                                [f"No UploadError on uploading {path}, "
        #                                 "but there should be"])
        #         passing_all = False

        return passing_all

    def execute(self, grades, module_dict, solution_dict):
        """Run student code.

        Overrides test_classes.TestCase.execute
        """
        upload_client = module_dict["upload_client"]
        client = upload_client.UploadClient(HOST, UPLOAD_PORT)
        passing_all = self._execute_helper(grades, client,
                                           upload_client.UploadError)
        client.close()
        return passing_all


class ListTest(UploadTest):
    """Test case for Question 5."""

    def execute(self, grades, module_dict, solution_dict):
        """Run student code.

        Overrides test_classes.TestCase.execute
        """
        upload_client = module_dict["upload_client"]
        client = upload_client.UploadClient(HOST, UPLOAD_PORT)
        passing_all = self._execute_helper(grades, client,
                                           upload_client.UploadError)

        uploaded_files = client.list_files()

        client.close()

        if len(uploaded_files) != len(self.good_files):
            self.add_fail_messages(grades,
                                   ["Incorrect number of results returned.",
                                    f"Returned {len(uploaded_files)}, but "
                                    "should have been {len(self.good_files)}"])
            return False

        for path, result in zip(self.good_files, uploaded_files):
            if ((type(result) != tuple or len(result) != 2 or
                 type(result[0]) != str or type(result[1]) != int)):
                self.add_fail_messages(
                    grades,
                    ["Should be receiving a list of (str, int) tuples"])
                return False

            file_name = os.path.basename(path)
            if file_name != result[0]:
                self.add_fail_messages(
                    grades,
                    ["File names not matching.",
                     f"Returned {result[0]}, but should have been {file_name}"]
                    )
                passing_all = False

            with open(path, "rb") as f:
                size = len(f.read())
                if size != result[1]:
                    self.add_fail_messages(
                        grades,
                        ["File sizes not matching.",
                         f"Returned {result[1]}, but should have been {size}"])
                    passing_all = False

        if passing_all:
            self.add_pass_message(grades)

        return passing_all
