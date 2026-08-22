import React from 'react';
import { DecisionFlow } from '../ndsp/DecisionFlow';

interface ApplicationShellProps {
  children?: React.ReactNode;
  pathname?: string;
}

export const ApplicationShell: React.FC<ApplicationShellProps> = ({ children }) => {
  return (
    <>
      <DecisionFlow />
      <div className="ndsp-app-shell min-h-screen bg-background text-foreground">
        <main className="w-full">
          {children}
        </main>
      </div>
    </>
  );
};
export default ApplicationShell;
