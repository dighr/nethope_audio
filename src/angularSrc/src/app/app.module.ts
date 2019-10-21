import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http'; 

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AudioTranscriptionComponent } from './pages/audio-transcription/audio-transcription.component';
import { ToolBarComponent} from './shared/tool-bar/tool-bar.component'

import { AudioTranscriptionService } from './services/audio-transcription.service'

import { from } from 'rxjs';

@NgModule({
   declarations: [
      AppComponent,
      AudioTranscriptionComponent,
      ToolBarComponent
   ],
   imports: [
      BrowserModule,
      AppRoutingModule,
      HttpClientModule
   ],
   providers: [],
   bootstrap: [
      AppComponent
   ]
})
export class AppModule { }
