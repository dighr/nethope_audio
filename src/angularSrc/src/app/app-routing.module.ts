import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AudioTranscriptionComponent } from './pages/audio-transcription/audio-transcription.component';


const routes: Routes = [
  {path: '', redirectTo: '/transcription', pathMatch: 'full'},
  {path: 'transcription', component: AudioTranscriptionComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
