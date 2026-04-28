import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';
import { ScreenshotsComponent } from './screenshots.component';

@NgModule({
  declarations: [ScreenshotsComponent],
  imports: [
    SharedModule,
    RouterModule.forChild([{ path: '', component: ScreenshotsComponent }]),
  ],
})
export class ScreenshotsModule {}
