import { createBrowserRouter } from 'react-router-dom'

import { AppShell } from '@/app/AppShell'
import { ChangesPage } from '@/pages/ChangesPage'
import { DocPage } from '@/pages/DocPage'
import { HomePage } from '@/pages/HomePage'
import { NotFoundPage } from '@/pages/NotFoundPage'
import { WireframePage } from '@/pages/WireframePage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppShell />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'changes', element: <ChangesPage /> },
      { path: 'doc/:no/:sec?/:flow?', element: <DocPage /> },
      { path: 'wireframe/:id?', element: <WireframePage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])
