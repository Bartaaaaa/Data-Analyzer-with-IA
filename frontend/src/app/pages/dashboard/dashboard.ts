import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { SpotifyService } from '../../services/spotifyService';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Dashboard {
  private fb = inject(FormBuilder);
  private router = inject(Router);
  private spotifyService = inject(SpotifyService);
  private route = inject(ActivatedRoute);

  loading = signal(false);
  error = signal<string | null>(null);

  isSpotifyConnected = false;
  spotifyToken = signal<string | null>(null);
  ngOnInit() {}

  spotifyRedirect() {
    this.router.navigate(['/spotifyDashboard']);
  }
}
