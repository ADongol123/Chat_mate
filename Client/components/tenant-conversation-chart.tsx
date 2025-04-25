"use client"

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts"

export function TenantConversationChart() {
  // Sample data for the chart
  const data = [
    { name: "Mon", conversations: 65, completionRate: 90 },
    { name: "Tue", conversations: 59, completionRate: 85 },
    { name: "Wed", conversations: 80, completionRate: 92 },
    { name: "Thu", conversations: 81, completionRate: 88 },
    { name: "Fri", conversations: 56, completionRate: 91 },
    { name: "Sat", conversations: 55, completionRate: 87 },
    { name: "Sun", conversations: 40, completionRate: 89 },
  ]

  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis yAxisId="left" />
          <YAxis yAxisId="right" orientation="right" domain={[0, 100]} />
          <Tooltip />
          <Legend />
          <Line yAxisId="left" type="monotone" dataKey="conversations" stroke="#8884d8" activeDot={{ r: 8 }} />
          <Line yAxisId="right" type="monotone" dataKey="completionRate" stroke="#82ca9d" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
