import React, { useState, useEffect, useRef } from 'react'
import { HomeOutlined, UploadOutlined, FileOutlined, BarChartOutlined, MenuOutlined, SettingOutlined, UserOutlined, LogoutOutlined } from '@ant-design/icons'
import '../../styles/Header.css'

const Header = ({ activeMenu, setActiveMenu, fetchDocuments, onAIClick }) => {
  const [sidebarVisible, setSidebarVisible] = useState(false)
  const sidebarRef = useRef(null)
  const toggleRef = useRef(null)
  
  const navItems = [
    { key: 'home', label: '首页', icon: <HomeOutlined /> },
    { key: 'documents', label: '文件', icon: <FileOutlined />, onClick: () => {
        fetchDocuments()
        setActiveMenu('documents')
      }},
    { key: 'analytics', label: '分析', icon: <BarChartOutlined /> }
  ]

  const sidebarItems = [
    { key: 'profile', label: '个人资料', icon: <UserOutlined /> },
    { key: 'ai-config', label: 'AI 服务配置', icon: <SettingOutlined /> },
    { key: 'logout', label: '退出登录', icon: <LogoutOutlined /> }
  ]

  const toggleSidebar = () => {
    setSidebarVisible(!sidebarVisible)
  }

  const handleClickOutside = (event) => {
    if (sidebarVisible && 
        sidebarRef.current && !sidebarRef.current.contains(event.target) &&
        toggleRef.current && !toggleRef.current.contains(event.target)) {
      setSidebarVisible(false)
    }
  }

  useEffect(() => {
    if (sidebarVisible) {
      document.addEventListener('mousedown', handleClickOutside)
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [sidebarVisible])

  return (
    <div className="header">
      <button 
        ref={toggleRef}
        className="sidebar-toggle"
        onClick={toggleSidebar}
      >
        <MenuOutlined />
      </button>
      
      <div 
        ref={sidebarRef}
        className={`sidebar ${sidebarVisible ? 'visible' : ''}`}
      >
        <div className="sidebar-content">
          <div className="sidebar-header">
            <h3>菜单</h3>
          </div>
          <div className="sidebar-menu">
            {sidebarItems.map((item) => (
              <button 
                key={item.key}
                className="sidebar-item"
                onClick={() => {
                  // 处理侧边栏项点击
                  console.log('Sidebar item clicked:', item.key)
                  if (item.key === 'ai-config' && onAIClick) {
                    onAIClick()
                  }
                  setSidebarVisible(false)
                }}
              >
                <span className="sidebar-item-icon">{item.icon}</span>
                <span className="sidebar-item-text">{item.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
      
      <div className="header-menu">
        {navItems.map((item) => (
          <button 
            key={item.key}
            className={`nav-button ${activeMenu === item.key ? 'active' : ''}`}
            onClick={item.onClick || (() => setActiveMenu(item.key))}
          >
            <span className="nav-button-icon">{item.icon}</span>
            <span className="nav-button-text">{item.label}</span>
          </button>
        ))}
      </div>
    </div>
  )
}

export default Header
