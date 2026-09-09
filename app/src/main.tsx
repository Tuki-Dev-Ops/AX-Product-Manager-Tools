import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { RouterProvider } from 'react-router-dom'

import { router } from '@/app/routes'
import '@/styles/tokens.css'
import '@/styles/base.css'

const el = document.getElementById('root')
if (!el) throw new Error('#root 요소를 찾지 못했습니다.')

createRoot(el).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
