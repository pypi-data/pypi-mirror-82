# Copyright (c) 2014 Prashanth Raghu
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from zaqar.storage.redis import catalogue
from zaqar.storage.redis import claims
from zaqar.storage.redis import flavors
from zaqar.storage.redis import messages
from zaqar.storage.redis import pools
from zaqar.storage.redis import queues
from zaqar.storage.redis import subscriptions

CatalogueController = catalogue.CatalogueController
ClaimController = claims.ClaimController
FlavorsController = flavors.FlavorsController
MessageController = messages.MessageController
QueueController = queues.QueueController
PoolsController = pools.PoolsController
SubscriptionController = subscriptions.SubscriptionController
