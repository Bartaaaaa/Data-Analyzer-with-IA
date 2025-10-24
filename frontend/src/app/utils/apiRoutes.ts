export const API_ROUTES = {
  auth: {
    login: '/auth/login',
    register: '/auth/register',
    checkAuth: '/auth/checkAuth',
    token: '/token',
  },
  user: {
    getMe: '/user',
    changeEmail: '/user/email',
  },
  demo: {
    root: '/demo',
  },
  connections: {
    spotifyConnection: '/spotify/auth/login',
    checkSpotifyConnection: '/spotify/auth/checkToken',
  },
} as const;
