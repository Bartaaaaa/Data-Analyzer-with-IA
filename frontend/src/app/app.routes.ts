import { Routes } from '@angular/router';
import { Login } from './pages/auth/login/login';
import { Register } from './pages/auth/register/register';
import { Connections } from './pages/connections/connections';
import { UserProfile } from './pages/userProfile/userProfile';
import { Dashboard } from './pages/dashboard/dashboard';
import { SpotifyDashboard } from './pages/dashboard/spotifyDashboard/spotifyDashboard';
export const routes: Routes = [
  { path: 'register', component: Register },
  { path: 'login', component: Login },
  { path: 'connections', component: Connections },
  { path: 'userProfile', component: UserProfile },
  { path: 'dashboard', component: Dashboard },
  { path: 'spotifyDashboard', component: SpotifyDashboard },
];
