import React from "react";

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return <div className="bg-white rounded-lg shadow p-4 text-sm text-red-600">Unable to load this view.</div>;
    }
    return this.props.children;
  }
}
