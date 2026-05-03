import { Injectable } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../../environments/environment";
import { Command, CommandCreate, CommandListResponse } from "../models/command.model";

@Injectable({ providedIn: "root" })
export class CommandService {
  private base = `${environment.apiUrl}/commands`;

  constructor(private http: HttpClient) {}

  createCommand(payload: CommandCreate): Observable<Command> {
    return this.http.post<Command>(`${this.base}/`, payload);
  }

  getCommandsByAgent(
    agentId: string,
    limit = 10,
    offset = 0,
    status?: string,
  ): Observable<CommandListResponse> {
    let params = new HttpParams()
      .set("agent_id", agentId)
      .set("limit", limit)
      .set("offset", offset);
    if (status) params = params.set("status", status);
    return this.http.get<CommandListResponse>(`${this.base}/`, { params });
  }

  getAllCommands(
    agentId?: string,
    status?: string,
    limit = 20,
    offset = 0,
  ): Observable<CommandListResponse> {
    let params = new HttpParams().set("limit", limit).set("offset", offset);
    if (agentId) params = params.set("agent_id", agentId);
    if (status) params = params.set("status", status);
    return this.http.get<CommandListResponse>(`${this.base}/`, { params });
  }
}
