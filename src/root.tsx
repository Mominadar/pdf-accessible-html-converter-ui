import { NextUIProvider } from '@nextui-org/react'
import './App.css'
import IndexPage from './pages'

function Root() {
  return (
    <NextUIProvider>
      <IndexPage/>
    </NextUIProvider>
  )
}

export default Root
