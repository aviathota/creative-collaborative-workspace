import React from 'react';
import 'static\\css\\mainpage.css';

const SidebarIcon = ({ icon, text }) => (
  <div className="sidebar-icon">
    <span className="icon">{icon}</span>
    <span className="text">{text}</span>
  </div>
);

const Sidebar = () => {
  return (
    <div className="sidebar">
      <SidebarIcon icon="👤" text="Profile" />
      <SidebarIcon icon="📁" text="Projects" />
      <SidebarIcon icon="📊" text="Tasks" />
      <SidebarIcon icon="✉️" text="Messages" />
    </div>
  );
};

const FileIcon = () => (
  <div className="file-icon">🗂️</div>
);

const FilesSection = () => {
  return (
    <div className="files">
        <div className="section-header">
          <FileIcon />
          <FileIcon />
          <FileIcon />
          <FileIcon />
        </div>
        <div className="add-file-icon">➕</div>
    </div>
  );
};

const Task = ({ goal, description, user }) => {
  return (
    <div className="task-item">
      <div><strong>Goal:</strong> {goal}</div>
      <div><strong>Description:</strong> {description}</div>
      <div><strong>User:</strong> {user}</div>
    </div>
  );
};

const TasksSection = ({ tasks }) => {
  return (
    <div className="tasks">
      {tasks.map(task => <Task key={task.id} {...task} />)}
      <div className="add-task">➕</div>
    </div>
  );
};

const ProjectDashboard = () => {
  const tasks = [
    { id: 1, goal: 'Goal 1', description: 'Description 1', user: 'User 1' },
    { id: 2, goal: 'Goal 2', description: 'Description 2', user: 'User 2' },
  ];

  return (
    <div className="container">
      <div className="header">
        CCW
      </div>
      <div className="main">
        <Sidebar />
        <div className="content">
          <div className="files-section">
            <div className="section-header">
              Files
            </div>
            <FilesSection />
          </div>
          <div className="tasks-section">
            <div className="section-header">
              Tasks
            </div>
            <TasksSection tasks={tasks} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectDashboard;
