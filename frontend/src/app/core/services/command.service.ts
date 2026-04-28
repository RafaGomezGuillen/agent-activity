import { Injectable } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../../environments/environment";
import { Command, CommandCreate } from "../models/command.model";

@Injectable({ providedIn: "root" })
export class CommandService {
  private base = `${environment.apiUrl}/commands`;

  constructor(private http: HttpClient) {}

  createCommand(payload: CommandCreate): Observable<Command> {
    return this.http.post<Command>(`${this.base}/`, payload);
  }

  getCommandsByAgent(agentId: string): Observable<Command[]> {
    let params = new HttpParams().set("agent_id", agentId);
    return this.http.get<Command[]>(`${this.base}/`, { params });
  }

  getAllCommands(
    agentId?: string,
    status?: string,
    page = 1,
    size = 20,
  ): Observable<Command[]> {
    let params = new HttpParams().set("page", page).set("size", size);
    if (agentId) params = params.set("agent_id", agentId);
    if (status) params = params.set("status", status);
    return this.http.get<Command[]>(`${this.base}/`, { params });
  }
}
