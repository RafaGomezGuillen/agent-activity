import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';
import { ClipboardsComponent } from './clipboards.component';

@NgModule({
  declarations: [ClipboardsComponent],
  imports: [
    SharedModule,
    RouterModule.forChild([{ path: '', component: ClipboardsComponent }]),
  ],
})
export class ClipboardsModule {}
