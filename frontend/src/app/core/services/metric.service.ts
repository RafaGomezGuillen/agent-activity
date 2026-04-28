import { Injectable } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../../environments/environment";
import { MetricFilters, MetricResponse } from "../models/metric.model";

@Injectable({ providedIn: "root" })
export class MetricService {
  private base = `${environment.apiUrl}/metrics`;

  constructor(private http: HttpClient) {}

  getMetrics(
    agentId: string,
    filters: MetricFilters = {},
  ): Observable<MetricResponse> {
    let params = new HttpParams();

    if (filters.start_time)
      params = params.set("start_time", filters.start_time);
    if (filters.end_time) params = params.set("end_time", filters.end_time);
    if (filters.limit !== undefined)
      params = params.set("limit", filters.limit);
    if (filters.offset !== undefined)
      params = params.set("offset", filters.offset);

    return this.http.get<MetricResponse>(`${this.base}/${agentId}`, { params });
  }
}
