import { Injectable } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../../environments/environment";
import { KeylogFilters, KeylogResponse } from "../models/keylog.model";

@Injectable({ providedIn: "root" })
export class KeylogService {
  private base = `${environment.apiUrl}/keylogs`;

  constructor(private http: HttpClient) {}

  getKeylogs(filters: KeylogFilters = {}): Observable<KeylogResponse> {
    let params = new HttpParams();

    if (filters.agent_id) params = params.set("agent_id", filters.agent_id);
    if (filters.start_time)
      params = params.set("start_time", filters.start_time);
    if (filters.end_time) params = params.set("end_time", filters.end_time);
    if (filters.app) params = params.set("app", filters.app);
    if (filters.type) params = params.set("type", filters.type);
    if (filters.limit !== undefined)
      params = params.set("limit", filters.limit);
    if (filters.offset !== undefined)
      params = params.set("offset", filters.offset);

    return this.http.get<KeylogResponse>(`${this.base}/`, { params });
  }

  downloadKeylogs(agentId: string) {
    return this.http.get(`${this.base}/download/${encodeURIComponent(agentId)}`, {
      observe: "response",
      responseType: "blob",
    });
  }
}
