from typing import List, Optional

import attr

from tdxapi.managers import helpers
from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.models.report import Report
from tdxapi.models.report_info import ReportInfo
from tdxapi.models.report_search import ReportSearch


@attr.s
class ReportManager(TdxManager):
    __tdx_section__ = "Reports"

    @tdx_method(
        "GET",
        "/api/reports/{id}"
        "?withData={withData}&dataSortExpression={dataSortExpression}",
    )
    def get(
        self,
        report_id: int,
        with_data: Optional[bool] = False,
        data_sort_expression: Optional[str] = None,
    ) -> Report:
        """Gets information about a report, optionally including data."""
        return self.dispatcher.send(
            self.get.method,
            self.get.url.format(
                id=report_id,
                withData=with_data,
                dataSortExpression=data_sort_expression or "",
            ),
            rclass=Report,
            rlist=False,
            rpartial=False,
        )

    @tdx_method("GET", "/api/reports")
    def get_all(self) -> List[ReportInfo]:
        """Gets a list of all Report Builder reports visible to the user."""
        return self.dispatcher.send(
            self.get_all.method,
            self.get_all.url,
            rclass=ReportInfo,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("POST", "/api/reports/search")
    def search(
        self,
        search_text: Optional[str] = None,
        for_app_id: Optional[int] = None,
        for_application_name: Optional[str] = None,
        owner_uid: Optional[str] = None,
        report_source_id: Optional[int] = None,
    ) -> List[ReportInfo]:
        """Gets a list of Report Builder reports visible to the user that match the
        provided search criteria.

        :param search_text: the search text to filter on. This will filter on the name
            of each report.
        :param for_app_id: the ID of the platform application to filter on. If
            specified, will only include reports belonging to this application.
        :param for_application_name: the name of the system application to filter on.
            If specified, will only include reports belonging to this application.
        :param owner_uid: the UID of the owner to filter on. If specified, will only
            return reports owned by this user.
        :param report_source_id: the ID of the report source to filter on. If
            specified, will only include reports belonging to this report source.
        """
        params = helpers.format_search_params(ReportSearch, self, locals())

        return self.dispatcher.send(
            self.search.method,
            self.search.url,
            data=params,
            rclass=ReportInfo,
            rlist=True,
            rpartial=True,
        )
