import React from "react";

export default function SkeletonBlock({ className = "h-24" }) {
  return <div className={`bg-gray-100 rounded-lg animate-pulse ${className}`} />;
}
