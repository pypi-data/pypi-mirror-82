#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

from collections import OrderedDict

import pytest

from marshmallow import ValidationError
from tests.utils import BaseTestCase, assert_equal_dict

from polyaxon import types
from polyaxon.polyflow.io import V1IO
from polyaxon.polyflow.params import ParamSpec, V1Param


@pytest.mark.polyflow_mark
class TestV1IOs(BaseTestCase):
    def test_wrong_io_config(self):
        # No name
        with self.assertRaises(ValidationError):
            V1IO.from_dict({})

    def test_unsupported_io_config_type(self):
        with self.assertRaises(ValidationError):
            V1IO.from_dict({"name": "input1", "type": "something"})

    def test_wrong_io_config_default(self):
        with self.assertRaises(ValidationError):
            V1IO.from_dict({"name": "input1", "type": types.FLOAT, "value": "foo"})

        with self.assertRaises(ValidationError):
            V1IO.from_dict({"name": "input1", "type": types.GCS, "value": 234})

    def test_wrong_io_config_flag(self):
        with self.assertRaises(ValidationError):
            V1IO.from_dict({"name": "input1", "type": types.S3, "isFlag": True})

        with self.assertRaises(ValidationError):
            V1IO.from_dict({"name": "input1", "type": types.FLOAT, "isFlag": True})

    def test_io_config_optionals(self):
        config_dict = {"name": "input1"}
        config = V1IO.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_io_config_desc(self):
        # test desc
        config_dict = {"name": "input1", "description": "some text"}
        config = V1IO.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_io_config_types(self):
        config_dict = {"name": "input1", "description": "some text", "type": types.INT}
        config = V1IO.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        expected_repr = OrderedDict((("name", "input1"), ("type", "int"), ("value", 3)))
        assert config.get_repr_from_value(3) == expected_repr
        assert config.get_repr() == OrderedDict((("name", "input1"), ("type", "int")))

        config_dict = {"name": "input1", "description": "some text", "type": types.S3}
        config = V1IO.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        expected_repr = OrderedDict(
            (("name", "input1"), ("type", types.S3), ("value", "s3://foo"))
        )
        assert config.get_repr_from_value("s3://foo") == expected_repr
        assert config.get_repr() == OrderedDict(
            (("name", "input1"), ("type", types.S3))
        )

    def test_io_config_default(self):
        config_dict = {
            "name": "input1",
            "description": "some text",
            "type": types.BOOL,
            "isOptional": True,
            "value": True,
        }
        config = V1IO.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        expected_repr = OrderedDict(
            (("name", "input1"), ("type", "bool"), ("value", True))
        )
        assert config.get_repr_from_value(None) == expected_repr
        assert config.get_repr() == expected_repr

        config_dict = {
            "name": "input1",
            "description": "some text",
            "type": types.FLOAT,
            "isOptional": True,
            "value": 3.4,
        }
        config = V1IO.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        expected_repr = OrderedDict(
            (("name", "input1"), ("type", "float"), ("value", 3.4))
        )
        assert config.get_repr_from_value(None) == expected_repr
        assert config.get_repr() == expected_repr

    def test_io_config_default_and_required(self):
        config_dict = {
            "name": "input1",
            "description": "some text",
            "type": types.BOOL,
            "value": True,
            "isOptional": True,
        }
        config = V1IO.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {
            "name": "input1",
            "description": "some text",
            "type": types.STR,
            "value": "foo",
        }
        with self.assertRaises(ValidationError):
            V1IO.from_dict(config_dict)

    def test_io_config_required(self):
        config_dict = {
            "name": "input1",
            "description": "some text",
            "type": "float",
            "isOptional": False,
        }
        config = V1IO.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        expected_repr = OrderedDict(
            (("name", "input1"), ("type", "float"), ("value", 1.1))
        )
        assert config.get_repr_from_value(1.1) == expected_repr
        assert config.get_repr() == OrderedDict((("name", "input1"), ("type", "float")))

    def test_io_config_flag(self):
        config_dict = {
            "name": "input1",
            "description": "some text",
            "type": types.BOOL,
            "isFlag": True,
        }
        config = V1IO.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        expected_repr = OrderedDict(
            (("name", "input1"), ("type", "bool"), ("value", False))
        )
        assert config.get_repr_from_value(False) == expected_repr

    def test_value_non_typed_input(self):
        config_dict = {"name": "input1"}
        config = V1IO.from_dict(config_dict)
        assert config.validate_value("foo") == "foo"
        assert config.validate_value(1) == 1
        assert config.validate_value(True) is True

        expected_repr = OrderedDict((("name", "input1"), ("value", "foo")))
        assert config.get_repr_from_value("foo") == expected_repr
        assert config.get_repr() == OrderedDict(name="input1")

    def test_value_typed_input(self):
        config_dict = {"name": "input1", "type": types.BOOL}
        config = V1IO.from_dict(config_dict)
        with self.assertRaises(ValidationError):
            config.validate_value("foo")
        with self.assertRaises(ValidationError):
            config.validate_value(1)
        with self.assertRaises(ValidationError):
            config.validate_value(None)

        assert config.validate_value(True) is True

    def test_value_typed_input_with_default(self):
        config_dict = {
            "name": "input1",
            "type": types.INT,
            "value": 12,
            "isOptional": True,
        }
        config = V1IO.from_dict(config_dict)
        with self.assertRaises(ValidationError):
            config.validate_value("foo")

        assert config.validate_value(1) == 1
        assert config.validate_value(0) == 0
        assert config.validate_value(-1) == -1
        assert config.validate_value(None) == 12
        expected_repr = OrderedDict(
            (("name", "input1"), ("type", "int"), ("value", 12))
        )
        assert config.get_repr_from_value(None) == expected_repr
        assert config.get_repr() == expected_repr

    def test_get_param(self):
        # None string values should exit fast
        param = V1Param(value=1)
        assert param.get_spec(
            name="foo",
            iotype=types.INT,
            is_flag=False,
            is_list=False,
            is_context=False,
            arg_format=None,
        ) == ParamSpec(
            name="foo",
            iotype=types.INT,
            param=param,
            is_flag=False,
            is_list=False,
            is_context=False,
            arg_format=None,
        )

        # Str values none regex
        param = V1Param(value="1")
        assert param.get_spec(
            name="foo",
            iotype=types.INT,
            is_flag=False,
            is_list=False,
            is_context=False,
            arg_format=None,
        ) == ParamSpec(
            name="foo",
            iotype=types.INT,
            param=param,
            is_flag=False,
            is_list=False,
            is_context=False,
            arg_format=None,
        )

        param = V1Param(value="SDfd")
        assert param.get_spec(
            name="foo",
            iotype=types.STR,
            is_flag=False,
            is_list=False,
            is_context=False,
            arg_format=None,
        ) == ParamSpec(
            name="foo",
            iotype=types.STR,
            param=param,
            is_flag=False,
            is_list=False,
            is_context=False,
            arg_format=None,
        )

        # Validation dag
        param = V1Param(value="inputs.foo", ref="dag")
        assert param.get_spec(
            name="foo",
            iotype=types.BOOL,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format=None,
        ) == ParamSpec(
            name="foo",
            iotype=types.BOOL,
            param=param,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format=None,
        )

        param = V1Param(value="{{ inputs }}", ref="dag")
        assert param.get_spec(
            name="foo",
            iotype=types.BOOL,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format=None,
        ) == ParamSpec(
            name="foo",
            iotype=types.BOOL,
            param=param,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format=None,
        )

        with self.assertRaises(ValidationError):
            param = V1Param(value="{{ outputs }}", ref="dag")
            param.get_spec(
                name="foo",
                iotype=types.BOOL,
                is_flag=True,
                is_list=False,
                is_context=False,
                arg_format=None,
            )

        with self.assertRaises(ValidationError):
            param = V1Param(value="inputs.foo", ref="dag.1")
            param.get_spec(
                name="foo",
                iotype=types.BOOL,
                is_flag=True,
                is_list=False,
                is_context=False,
                arg_format=None,
            )

        # Validation ops
        param = V1Param(value="{{ outputs.foo }}", ref="ops.foo-bar")
        assert param.get_spec(
            name="foo",
            iotype=types.BOOL,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format=None,
        ) == ParamSpec(
            name="foo",
            iotype=types.BOOL,
            param=param,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format=None,
        )

        param = V1Param(value="inputs.foo", ref="ops.foo-bar")
        assert param.get_spec(
            name="foo",
            iotype=types.BOOL,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format=None,
        ) == ParamSpec(
            name="foo",
            iotype=types.BOOL,
            param=param,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format=None,
        )

        param = V1Param(value="inputs", ref="ops.foo-bar")
        assert param.get_spec(
            name="foo",
            iotype=types.BOOL,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format=None,
        ) == ParamSpec(
            name="foo",
            iotype=types.BOOL,
            param=param,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format=None,
        )

        # Regex validation ops: invalid params
        with self.assertRaises(ValidationError):
            param = V1Param(value="status.foo", ref="ops.foo-bar")
            param.get_spec(
                name="foo",
                iotype=types.BOOL,
                is_flag=True,
                is_list=False,
                is_context=False,
                arg_format=None,
            )

        # Validation runs
        uid = uuid.uuid4().hex
        param = V1Param(value="outputs.foo", ref="runs.{}".format(uid))
        assert param.get_spec(
            name="foo",
            iotype=types.BOOL,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format=None,
        ) == ParamSpec(
            name="foo",
            iotype=types.BOOL,
            param=param,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format=None,
        )

        uid = uuid.uuid4().hex
        param = V1Param(value="inputs.foo", ref="runs.{}".format(uid))
        assert param.get_spec(
            name="foo",
            iotype=types.BOOL,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format=None,
        ) == ParamSpec(
            name="foo",
            iotype=types.BOOL,
            param=param,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format=None,
        )

        # Custom arg_format
        param = V1Param(value="SDfd")
        assert param.get_spec(
            name="foo",
            iotype=types.STR,
            is_flag=False,
            is_list=False,
            is_context=False,
            arg_format="--sdf={foo}",
        ) == ParamSpec(
            name="foo",
            iotype=types.STR,
            param=param,
            is_flag=False,
            is_list=False,
            is_context=False,
            arg_format="--sdf={foo}",
        )
        assert (
            ParamSpec(
                name="foo",
                iotype=types.STR,
                param=param,
                is_flag=False,
                is_list=False,
                is_context=False,
                arg_format="--sdf={foo}",
            ).as_arg()
            == "--sdf=SDfd"
        )

        # Custom arg_format with empty value
        param = V1Param(value=None)
        assert param.get_spec(
            name="foo",
            iotype=types.STR,
            is_flag=False,
            is_list=False,
            is_context=False,
            arg_format="--sdf={foo}",
        ) == ParamSpec(
            name="foo",
            iotype=types.STR,
            param=param,
            is_flag=False,
            is_list=False,
            is_context=False,
            arg_format="--sdf={foo}",
        )
        assert (
            ParamSpec(
                name="foo",
                iotype=types.STR,
                param=param,
                is_flag=False,
                is_list=False,
                is_context=False,
                arg_format="--sdf={foo}",
            ).as_arg()
            == ""
        )

        # isFlag
        param = V1Param(value=True)
        assert param.get_spec(
            name="foo",
            iotype=types.STR,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format="{foo}",
        ) == ParamSpec(
            name="foo",
            iotype=types.STR,
            param=param,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format="{foo}",
        )
        assert (
            str(
                ParamSpec(
                    name="foo",
                    iotype=types.STR,
                    param=param,
                    is_flag=True,
                    is_list=False,
                    is_context=False,
                    arg_format="{foo}",
                )
            )
            == "--foo"
        )

        # isFlag empty
        param = V1Param(value=None)
        assert param.get_spec(
            name="foo",
            iotype=types.STR,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format="{foo}",
        ) == ParamSpec(
            name="foo",
            iotype=types.STR,
            param=param,
            is_flag=True,
            is_list=False,
            is_context=False,
            arg_format="{foo}",
        )
        assert (
            str(
                ParamSpec(
                    name="foo",
                    iotype=types.STR,
                    param=param,
                    is_flag=True,
                    is_list=False,
                    is_context=False,
                    arg_format="{foo}",
                )
            )
            == ""
        )

        # isContext
        param = V1Param(value={"key": "value"})
        assert param.get_spec(
            name="foo",
            iotype=types.STR,
            is_flag=False,
            is_list=False,
            is_context=True,
            arg_format="{foo}",
        ) == ParamSpec(
            name="foo",
            iotype=types.STR,
            param=param,
            is_flag=False,
            is_list=False,
            is_context=True,
            arg_format="{foo}",
        )
        assert ParamSpec(
            name="foo",
            iotype=types.STR,
            param=param,
            is_flag=False,
            is_list=False,
            is_context=True,
            arg_format=None,
        ).param.value == {"key": "value"}
        assert str(
            ParamSpec(
                name="foo",
                iotype=types.STR,
                param=param,
                is_flag=False,
                is_list=False,
                is_context=True,
                arg_format=None,
            )
        ) == str({"key": "value"})

        # Regex validation runs: invalid params
        with self.assertRaises(ValidationError):
            param = V1Param(value="outputs.foo", ref="run.foo-bar")
            param.get_spec(
                name="foo",
                iotype=types.BOOL,
                is_flag=True,
                is_list=False,
                is_context=False,
                arg_format=None,
            )
