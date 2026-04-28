import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';
import { DocsComponent } from './docs.component';

@NgModule({
  declarations: [DocsComponent],
  imports: [
    SharedModule,
    RouterModule.forChild([{ path: '', component: DocsComponent }]),
  ],
})
export class DocsModule {}
