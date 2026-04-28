import { Injectable } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../../environments/environment";
import { Agent, AgentFilters, AgentPagination } from "../models/agent.model";

@Injectable({ providedIn: "root" })
export class AgentService {
  private base = `${environment.apiUrl}/agents`;

  constructor(private http: HttpClient) {}

  getAgents(
    page = 1,
    size = 12,
    filters: AgentFilters = {},
  ): Observable<AgentPagination> {
    let params = new HttpParams().set("page", page).set("size", size);

    if (filters.search) params = params.set("search", filters.search);
    if (filters.os) params = params.set("os", filters.os);
    if (filters.status !== null && filters.status !== undefined) {
      params = params.set("status", String(filters.status));
    }

    return this.http.get<AgentPagination>(`${this.base}/`, { params });
  }

  getAgent(id: string): Observable<Agent> {
    return this.http.get<Agent>(`${this.base}/${id}`);
  }
}
