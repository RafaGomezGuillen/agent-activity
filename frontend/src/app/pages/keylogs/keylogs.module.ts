import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';
import { KeylogsComponent } from './keylogs.component';

@NgModule({
  declarations: [KeylogsComponent],
  imports: [
    SharedModule,
    RouterModule.forChild([{ path: '', component: KeylogsComponent }]),
  ],
})
export class KeylogsModule {}
