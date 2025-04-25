import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Bot, MoreVertical, Edit, Trash2, Eye, Copy, Plus } from "lucide-react"

interface TenantChatbotListProps {
  limit?: number
}

export function TenantChatbotList({ limit }: TenantChatbotListProps) {
  // Sample chatbot data
  const chatbots = [
    {
      id: "1",
      name: "Customer Support Bot",
      status: "published",
      interactions: 845,
      createdAt: "2023-06-12T00:00:00.000Z",
    },
    {
      id: "2",
      name: "Sales Assistant",
      status: "published",
      interactions: 324,
      createdAt: "2023-07-18T00:00:00.000Z",
    },
    {
      id: "3",
      name: "Product Recommender",
      status: "draft",
      interactions: 0,
      createdAt: "2023-08-24T00:00:00.000Z",
    },
    {
      id: "4",
      name: "FAQ Bot",
      status: "archived",
      interactions: 115,
      createdAt: "2023-05-30T00:00:00.000Z",
    },
  ]

  const displayChatbots = limit ? chatbots.slice(0, limit) : chatbots

  return (
    <div className="space-y-4">
      <div className="rounded-md border">
        <div className="grid grid-cols-12 gap-4 p-4 text-sm font-medium text-muted-foreground">
          <div className="col-span-4">Chatbot</div>
          <div className="col-span-3">Status</div>
          <div className="col-span-2">Interactions</div>
          <div className="col-span-2">Created</div>
          <div className="col-span-1"></div>
        </div>
        {displayChatbots.map((chatbot) => (
          <div key={chatbot.id} className="grid grid-cols-12 gap-4 border-t p-4 text-sm">
            <div className="col-span-4 flex items-center gap-3">
              <Avatar className="h-8 w-8">
                <AvatarImage src={`/placeholder.svg?height=32&width=32`} alt={chatbot.name} />
                <AvatarFallback>
                  <Bot className="h-4 w-4" />
                </AvatarFallback>
              </Avatar>
              <div className="font-medium">{chatbot.name}</div>
            </div>
            <div className="col-span-3 flex items-center">
              <Badge
                variant={
                  chatbot.status === "published" ? "success" : chatbot.status === "draft" ? "outline" : "secondary"
                }
                className="capitalize"
              >
                {chatbot.status}
              </Badge>
            </div>
            <div className="col-span-2 flex items-center">{chatbot.interactions}</div>
            <div className="col-span-2 flex items-center">{new Date(chatbot.createdAt).toLocaleDateString()}</div>
            <div className="col-span-1 flex items-center justify-end">
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="icon" className="h-8 w-8">
                    <MoreVertical className="h-4 w-4" />
                    <span className="sr-only">Open menu</span>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuLabel>Actions</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem>
                    <Eye className="mr-2 h-4 w-4" />
                    <span>View Chatbot</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <Edit className="mr-2 h-4 w-4" />
                    <span>Edit Chatbot</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <Copy className="mr-2 h-4 w-4" />
                    <span>Duplicate</span>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem className="text-destructive">
                    <Trash2 className="mr-2 h-4 w-4" />
                    <span>Delete Chatbot</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        ))}
      </div>
      {!limit && (
        <div className="flex items-center justify-between py-4">
          <Button variant="outline">
            <Plus className="mr-2 h-4 w-4" />
            New Chatbot
          </Button>
          <div className="flex items-center space-x-2">
            <Button variant="outline" size="sm">
              Previous
            </Button>
            <Button variant="outline" size="sm">
              Next
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
