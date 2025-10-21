export const API_ROUTES = {
  auth: {
    login: '/login',
    register: '/register',
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
    checkSpotifyConnection: '/spotify/checkToken',
  },
} as const;
