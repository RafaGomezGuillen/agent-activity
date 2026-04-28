import { Component } from '@angular/core';
import { ThemeService } from '../../core/services/theme.service';

@Component({
  selector: 'app-topbar',
  templateUrl: './topbar.html',
  standalone: false,
  styles: [],
})
export class TopbarComponent {
  constructor(public themeService: ThemeService) {}
}
