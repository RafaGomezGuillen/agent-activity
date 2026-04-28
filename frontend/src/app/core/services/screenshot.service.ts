import { Injectable } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../../environments/environment";
import {
  ScreenshotFilters,
  ScreenshotResponse,
} from "../models/screenshot.model";

@Injectable({ providedIn: "root" })
export class ScreenshotService {
  private base = `${environment.apiUrl}/screenshots`;

  constructor(private http: HttpClient) {}

  getScreenshots(
    filters: ScreenshotFilters = {},
  ): Observable<ScreenshotResponse> {
    let params = new HttpParams();

    if (filters.agent_id) params = params.set("agent_id", filters.agent_id);
    if (filters.start_time)
      params = params.set("start_time", filters.start_time);
    if (filters.end_time) params = params.set("end_time", filters.end_time);
    if (filters.limit !== undefined)
      params = params.set("limit", filters.limit);
    if (filters.offset !== undefined)
      params = params.set("offset", filters.offset);

    return this.http.get<ScreenshotResponse>(`${this.base}/`, { params });
  }

  getScreenshotFileUrl(screenshotId: string): string {
    return `${this.base}/file/${screenshotId}`;
  }
}
