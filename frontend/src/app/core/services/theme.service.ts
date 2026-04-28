import { Injectable, Inject, PLATFORM_ID } from "@angular/core";

@Injectable({ providedIn: "root" })
export class ThemeService {
  private readonly STORAGE_KEY = "theme";
  private _isDark = true;

  constructor(@Inject(PLATFORM_ID) private platformId: object) {
    this.initTheme();
  }

  get isDark(): boolean {
    return this._isDark;
  }

  initTheme(): void {
    const saved = localStorage.getItem(this.STORAGE_KEY);
    this._isDark = saved === null ? true : saved === "dark";
    this.applyTheme();
  }

  toggle(): void {
    this._isDark = !this._isDark;
    localStorage.setItem(this.STORAGE_KEY, this._isDark ? "dark" : "light");
    this.applyTheme();
  }

  setDark(dark: boolean): void {
    this._isDark = dark;
    localStorage.setItem(this.STORAGE_KEY, dark ? "dark" : "light");
    this.applyTheme();
  }

  private applyTheme(): void {
    const html = document.documentElement;
    if (this._isDark) {
      html.classList.add("dark");
    } else {
      html.classList.remove("dark");
    }
  }
}
