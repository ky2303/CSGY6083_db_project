import React, { lazy, Suspense } from 'react';
import {Routes, Route } from 'react-router-dom'
import NavBar from './Components/NavBar';

const NoMatch = lazy(() => import('./Components/NoMatch'));
const Home = lazy (() => import('./Pages/Home'));
const Report = lazy (() => import('./Pages/Report'));
const GroupDetails = lazy (() => import('./Pages/GroupDetails'));

const App = () => {
  return (
    <>
        <NavBar />
        <div className="container">
            <Suspense fallback={<div className='container'>Loading...</div>}>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/report" element={<Report />} />
                    <Route path="/groups/:slug" element={<GroupDetails />} />
                    <Route path="*" element={<NoMatch />} />
                </Routes>
            </Suspense>
        </div>
    </>
  )
}

export default App;