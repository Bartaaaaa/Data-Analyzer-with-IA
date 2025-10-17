export const API_ROUTES = {
  auth: {
    login: '/login',
    register: '/register',
    checkAuth: '/auth/checkAuth',
  },
  user: {
    getMe: '/user',
    changeEmail: '/user/email',
  },
  demo: {
    root: '/demo',
  },
  connections: {
    connections: '/connections',
  },
} as const;
