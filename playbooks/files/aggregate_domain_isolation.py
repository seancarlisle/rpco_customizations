# Copyright (c) 2011-2013 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_log import log as logging

from nova.scheduler import filters
from nova.scheduler.filters import utils


LOG = logging.getLogger(__name__)


class AggregateDomainIsolationFilter(filters.BaseHostFilter):
    """Isolate tenants in specific aggregates."""

    # Aggregate data and tenant do not change within a request
    run_filter_once_per_request = True

    def host_passes(self, host_state, spec_obj):
        """If a host is in an aggregate that has the metadata key
        "filter_tenant_id" it can only create instances from that tenant(s).
        A host can be in different aggregates.

        If a host doesn't belong to an aggregate with the metadata key
        "filter_tenant_id" it can create instances from all tenants.
        """
	#import ipdb; ipdb.set_trace()

        tenant_id = spec_obj.project_id
	LOG.debug("Spec: %s" % spec_obj)

        metadata = utils.aggregate_metadata_get_by_host(host_state,
                                                        key="domain_tenant_ids")

        if metadata != {}:
            configured_tenant_ids = metadata.get("domain_tenant_ids")
	    LOG.debug("%s %s", tenant_id, configured_tenant_ids)
            if configured_tenant_ids:
                if tenant_id in configured_tenant_ids:
                    LOG.debug("Host tenant id %s matched", tenant_id)
		    return True
		else:
                    LOG.debug("%s fails tenant id on aggregate", host_state)
                    return False
            else:
                LOG.debug("No tenant id's defined on host. Host passes.")
        return True
