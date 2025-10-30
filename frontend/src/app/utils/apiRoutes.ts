export const API_ROUTES = {
  auth: {
    login: '/auth/login',
    register: '/auth/register',
    checkAuth: '/auth/checkAuth',
  },
  user: {
    getMe: '/users/me',
    changeEmail: '/user/email',
  },
  demo: {
    root: '/demo',
  },
  connections: {
    spotifyConnection: '/spotify/auth/login',
    checkSpotifyConnection: '/spotify/auth/checkToken',
  },
  spotify: {
    topArtists: '/spotify/userdata/topArtists',
    topTracks: '/spotify/userdata/topTracks',
  },
} as const;
