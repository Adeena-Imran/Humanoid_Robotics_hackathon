import React from "react";
import Layout from "@theme/Layout";
import AuthForm from "../components/AuthForm"; // Import AuthForm

export default function SignInPage() {
  return (
    <Layout
      title="Sign In"
      description="Sign In or Sign Up to access authenticated features."
    >
      <main className="container margin-vert--lg">
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
          <AuthForm />
        </div>
      </main>
    </Layout>
  );
}