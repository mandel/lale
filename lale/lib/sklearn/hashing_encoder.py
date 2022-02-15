# Copyright 2019 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import scipy.sparse.csr

from category_encoders.hashing import HashingEncoder 

import lale.docstrings
import lale.operators

_hyperparams_schema = {
            "allOf": [
                {
                    "type": "object",
                    "properties": {},
                    "relevantToOptimizer": [],
                }
            ]
        }
# _hyperparams_schema = {
#     "description": "Hyperparameter schema for the HashingEncoder model from scikit-learn contrib.",
#     "allOf": [
#         {
#             "description": "This first object lists all constructor arguments with their types, but omits constraints for conditional hyperparameters.",
#             "type": "object",
#             "additionalProperties": False,
#             "required": ["categories", "sparse", "dtype", "handle_unknown"],
#             "relevantToOptimizer": [],
#             "properties": {
#                 "categories": {
#                     "anyOf": [
#                         {
#                             "description": "Determine categories automatically from training data.",
#                             "enum": ["auto", None],
#                         },
#                         {
#                             "description": "The ith list element holds the categories expected in the ith column.",
#                             "type": "array",
#                             "items": {
#                                 "anyOf": [
#                                     {
#                                         "type": "array",
#                                         "items": {"type": "string"},
#                                     },
#                                     {
#                                         "type": "array",
#                                         "items": {"type": "number"},
#                                         "description": "Should be sorted.",
#                                     },
#                                 ]
#                             },
#                         },
#                     ],
#                     "default": "auto",
#                 },
#                 "sparse": {
#                     "description": "Will return sparse matrix if set true, else array.",
#                     "type": "boolean",
#                     "default": True,
#                 },
#                 "dtype": {
#                     "description": "Desired dtype of output, must be number. See https://docs.scipy.org/doc/numpy-1.14.0/reference/arrays.scalars.html#arrays-scalars-built-in",
#                     "laleType": "Any",
#                     "default": "float64",
#                 },
#                 "handle_unknown": {
#                     "description": "Whether to raise an error or ignore if an unknown categorical feature is present during transform.",
#                     "enum": ["error", "ignore"],
#                     "default": "error",
#                 },
#             },
#         }
#     ],
# }

_input_fit_schema = {
    "type": "object",
    "required": ["X"],
    "additionalProperties": False,
    "properties": {
        "X": {
            "description": "Features; the outer array is over samples.",
            "type": "array",
            "items": {
                "type": "array",
                "items": {"anyOf": [{"type": "number"}, {"type": "string"}]},
            },
        },
        "y": {"description": "Target class labels; the array is over samples."},
    },
}

_input_transform_schema = {
    "type": "object",
    "required": ["X"],
    "additionalProperties": False,
    "properties": {
        "X": {
            "description": "Features; the outer array is over samples.",
            "type": "array",
            "items": {
                "type": "array",
                "items": {"anyOf": [{"type": "number"}, {"type": "string"}]},
            },
        }
    },
}

_output_transform_schema = {
    "description": "Hash codes.",
    "type": "array",
    "items": {"type": "array", "items": {"type": "number"}},
}

_combined_schemas = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": """`Hashing encoder`_ transformer from scikit-learn contrib that encodes categorical features as numbers.

.. _`Hashing encoder`: https://contrib.scikit-learn.org/category_encoders/hashing.html
""",
    "documentation_url": "https://lale.readthedocs.io/en/latest/modules/lale.lib.sklearn.hashing_encoder.html",
    "import_from": "category_encoders.hashing",
    "type": "object",
    "tags": {"pre": ["categoricals"], "op": ["transformer"], "post": []},
    "properties": {
        "hyperparams": _hyperparams_schema,
        "input_fit": _input_fit_schema,
        "input_transform": _input_transform_schema,
        "output_transform": _output_transform_schema,
    },
}


class _HashingEncoderImpl:
    def __init__(self, **hyperparams):
        self._hyperparams = hyperparams
        self._wrapped_model = HashingEncoder(**self._hyperparams)

    def fit(self, X, y=None):
        self._wrapped_model.fit(X, y)
        if isinstance(X, pd.DataFrame):
            self._X_columns = X.columns
        return self

    def transform(self, X):
        result = self._wrapped_model.transform(X)
        return result


HashingEncoder = lale.operators.make_operator(_HashingEncoderImpl, _combined_schemas)

lale.docstrings.set_docstrings(HashingEncoder)
