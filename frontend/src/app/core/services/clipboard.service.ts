import { Injectable } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../../environments/environment";
import { ClipboardFilters, ClipboardResponse } from "../models/clipboard.model";

@Injectable({ providedIn: "root" })
export class ClipboardService {
  private base = `${environment.apiUrl}/clipboards`;

  constructor(private http: HttpClient) {}

  getClipboards(filters: ClipboardFilters = {}): Observable<ClipboardResponse> {
    let params = new HttpParams();

    if (filters.agent_id) params = params.set("agent_id", filters.agent_id);
    if (filters.start_time)
      params = params.set("start_time", filters.start_time);
    if (filters.end_time) params = params.set("end_time", filters.end_time);
    if (filters.app) params = params.set("app", filters.app);
    if (filters.limit !== undefined)
      params = params.set("limit", filters.limit);
    if (filters.offset !== undefined)
      params = params.set("offset", filters.offset);

    return this.http.get<ClipboardResponse>(`${this.base}/`, { params });
  }

  downloadClipboards(agentId: string) {
    return this.http.get(`${this.base}/download/${encodeURIComponent(agentId)}`, {
      observe: "response",
      responseType: "blob",
    });
  }
}
