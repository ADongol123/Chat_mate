"use client"

import { useState } from "react"
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Bot, MessageSquare, ShoppingCart, HelpCircle } from "lucide-react"
import { cn } from "@/lib/utils"

export function ChatbotTemplateSelector() {
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null)

  const templates = [
    {
      id: "customer-support",
      title: "Customer Support",
      description: "Handle customer inquiries and support requests",
      icon: <MessageSquare className="h-8 w-8" />,
    },
    {
      id: "sales-assistant",
      title: "Sales Assistant",
      description: "Help customers find and purchase products",
      icon: <ShoppingCart className="h-8 w-8" />,
    },
    {
      id: "faq-bot",
      title: "FAQ Bot",
      description: "Answer frequently asked questions",
      icon: <HelpCircle className="h-8 w-8" />,
    },
    {
      id: "blank",
      title: "Blank Template",
      description: "Start from scratch with no predefined settings",
      icon: <Bot className="h-8 w-8" />,
    },
  ]

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
      {templates.map((template) => (
        <Card
          key={template.id}
          className={cn(
            "cursor-pointer transition-all hover:border-primary",
            selectedTemplate === template.id && "border-2 border-primary",
          )}
          onClick={() => setSelectedTemplate(template.id)}
        >
          <CardHeader className="p-4">
            <div className="flex items-center gap-3">
              <div className="rounded-md bg-primary/10 p-2 text-primary">{template.icon}</div>
              <div>
                <CardTitle className="text-base">{template.title}</CardTitle>
                <CardDescription className="text-xs">{template.description}</CardDescription>
              </div>
            </div>
          </CardHeader>
        </Card>
      ))}
    </div>
  )
}
