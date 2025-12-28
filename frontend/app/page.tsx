"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import {
  Send,
  ShoppingCart,
  Plus,
  Minus,
  X,
  Menu,
  MessageSquarePlus,
  Trash2,
  Lock,
  CreditCard,
  Package,
  Check,
} from "lucide-react"

interface Product {
  id: number
  title: string
  price: number
  image: string
  rating: number
  badge?: string
  description?: string
}

interface CartItem extends Product {
  quantity: number
}

interface Message {
  role: "user" | "assistant"
  content: string
  products?: Product[]
  type?: "text" | "shipping-form" | "payment-form" | "success"
}

interface Conversation {
  id: string
  title: string
  messages: Message[]
}

const mockProducts: Product[] = [
  {
    id: 1,
    title: "Premium Travel Luggage Set",
    price: 89.99,
    image: "/modern-black-luggage-suitcase.jpg",
    rating: 4.8,
    badge: "Best Seller",
    description: "A complete set of durable and stylish luggage for all your travel needs.",
  },
  {
    id: 2,
    title: "Expandable Carry-On Suitcase",
    price: 64.99,
    image: "/blue-carry-on-suitcase.jpg",
    rating: 4.6,
    description: "Lightweight and expandable carry-on, perfect for short trips.",
  },
  {
    id: 3,
    title: "Lightweight Travel Backpack",
    price: 39.99,
    image: "/grey-travel-backpack.jpg",
    rating: 4.9,
    badge: "Top Rated",
    description: "Ergonomic and spacious backpack for comfortable travel.",
  },
  {
    id: 4,
    title: 'Hard Shell Luggage 28"',
    price: 94.99,
    image: "/silver-hardshell-luggage.jpg",
    rating: 4.7,
    description: "Robust hard shell luggage with ample space and security.",
  },
]

export default function ShoppingAssistant() {
  const [conversations, setConversations] = useState<Conversation[]>([
    {
      id: "1",
      title: "New Chat",
      messages: [
        {
          role: "assistant",
          content:
            "Hello! I'm your personal shopping assistant. I can help you find the perfect luggage for your travels. What are you looking for today?",
        },
      ],
    },
  ])
  const [currentConversationId, setCurrentConversationId] = useState("1")
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [cart, setCart] = useState<CartItem[]>([])
  const [isCartOpen, setIsCartOpen] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)
  const [isInCheckoutFlow, setIsInCheckoutFlow] = useState(false)
  const [checkoutStep, setCheckoutStep] = useState<"shipping" | "payment" | "complete">("shipping")
  const [isProcessingPayment, setIsProcessingPayment] = useState(false)
  const [shippingInfo, setShippingInfo] = useState({
    firstName: "",
    lastName: "",
    email: "",
    address: "",
    city: "",
    zipCode: "",
  })
  const [paymentInfo, setPaymentInfo] = useState({
    cardNumber: "",
    expiryDate: "",
    cvv: "",
  })
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const currentConversation = conversations.find((c) => c.id === currentConversationId)!

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [currentConversation.messages])

  const addToCart = (product: Product) => {
    setCart((prev) => {
      const existingItem = prev.find((item) => item.id === product.id)
      if (existingItem) {
        return prev.map((item) => (item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item))
      }
      return [...prev, { ...product, quantity: 1 }]
    })
  }

  const removeFromCart = (productId: string) => {
    setCart((prev) => prev.filter((item) => item.id !== Number(productId)))
  }

  const updateQuantity = (productId: string, change: number) => {
    setCart((prev) =>
      prev
        .map((item) => (item.id === Number(productId) ? { ...item, quantity: item.quantity + change } : item))
        .filter((item) => item.quantity > 0),
    )
  }

  const cartTotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0)
  const cartItemCount = cart.reduce((sum, item) => sum + item.quantity, 0)

  const updateCurrentConversation = (updater: (conv: Conversation) => Conversation) => {
    setConversations((prevConversations) =>
      prevConversations.map((conv) => (conv.id === currentConversationId ? updater(conv) : conv)),
    )
  }

  const createNewConversation = () => {
    const newId = Date.now().toString()
    const newConv: Conversation = {
      id: newId,
      title: "New Chat",
      messages: [
        {
          role: "assistant",
          content:
            "Hello! I'm your personal shopping assistant. I can help you find the perfect luggage for your travels. What are you looking for today?",
        },
      ],
    }
    setConversations([...conversations, newConv])
    setCurrentConversationId(newId)
    setIsInCheckoutFlow(false)
  }

  const deleteConversation = (id: string) => {
    const filtered = conversations.filter((c) => c.id !== id)
    if (filtered.length === 0) {
      createNewConversation()
    } else {
      setConversations(filtered)
      if (currentConversationId === id) {
        setCurrentConversationId(filtered[0].id)
      }
    }
  }

  const startCheckoutFlow = () => {
    if (cart.length === 0) {
      updateCurrentConversation((conv) => ({
        ...conv,
        messages: [
          ...conv.messages,
          {
            role: "assistant",
            content: "Your cart is empty! Please add some products first before checking out.",
          },
        ],
      }))
      return
    }

    setIsInCheckoutFlow(true)
    setCheckoutStep("shipping")
    updateCurrentConversation((conv) => ({
      ...conv,
      messages: [
        ...conv.messages,
        {
          role: "assistant",
          content: `Great! Let's complete your order of ${cartItemCount} item(s) totaling $${cartTotal.toFixed(2)}. First, I'll need your shipping information.`,
          type: "shipping-form",
        },
      ],
    }))
  }

  const handleShippingSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setCheckoutStep("payment")
    updateCurrentConversation((conv) => ({
      ...conv,
      messages: [
        ...conv.messages,
        {
          role: "assistant",
          content: `Perfect! Shipping to ${shippingInfo.address}, ${shippingInfo.city}. Now, let's complete the payment.`,
          type: "payment-form",
        },
      ],
    }))
  }

  const handlePayment = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsProcessingPayment(true)

    // Simulate payment processing
    await new Promise((resolve) => setTimeout(resolve, 2500))

    setIsProcessingPayment(false)
    setCheckoutStep("complete")

    updateCurrentConversation((conv) => ({
      ...conv,
      messages: [
        ...conv.messages,
        {
          role: "assistant",
          content: `Payment successful! Your order has been confirmed. We'll send a confirmation email to ${shippingInfo.email}. Thank you for shopping with us!`,
          type: "success",
        },
      ],
    }))

    // Clear cart after successful payment
    setTimeout(() => {
      setCart([])
      setIsInCheckoutFlow(false)
      setShippingInfo({
        firstName: "",
        lastName: "",
        email: "",
        address: "",
        city: "",
        zipCode: "",
      })
      setPaymentInfo({
        cardNumber: "",
        expiryDate: "",
        cvv: "",
      })
    }, 1000)
  }

  const formatCardNumber = (value: string) => {
    const cleaned = value.replace(/\s/g, "")
    const formatted = cleaned.match(/.{1,4}/g)?.join(" ") || cleaned
    return formatted.slice(0, 19)
  }

  const formatExpiryDate = (value: string) => {
    const cleaned = value.replace(/\D/g, "")
    if (cleaned.length >= 2) {
      return cleaned.slice(0, 2) + "/" + cleaned.slice(2, 4)
    }
    return cleaned
  }

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return

    const userMessage = input.trim()
    setInput("")
    setIsLoading(true)

    updateCurrentConversation((conv) => ({
      ...conv,
      title: conv.messages.length === 1 ? userMessage.slice(0, 30) : conv.title,
      messages: [...conv.messages, { role: "user", content: userMessage }],
    }))

    const checkoutKeywords = ["checkout", "pay", "payment", "buy", "purchase", "proceed to payment"]
    if (checkoutKeywords.some((keyword) => userMessage.toLowerCase().includes(keyword))) {
      setIsLoading(false)
      startCheckoutFlow()
      return
    }

    // Handle "add to cart" commands
    const addToCartMatch = userMessage.match(/add.*?(\d+).*?cart/i)
    if (addToCartMatch) {
      const productIndex = Number.parseInt(addToCartMatch[1]) - 1
      if (productIndex >= 0 && productIndex < mockProducts.length) {
        addToCart(mockProducts[productIndex])
        updateCurrentConversation((conv) => ({
          ...conv,
          messages: [
            ...conv.messages,
            {
              role: "assistant",
              content: `Great choice! I've added ${mockProducts[productIndex].title} to your cart. Would you like to continue shopping or proceed to checkout?`,
            },
          ],
        }))
        setIsLoading(false)
        return
      }
    }

    setTimeout(() => {
      let response = ""
      let products: Product[] = []

      if (userMessage.toLowerCase().includes("luggage") || userMessage.toLowerCase().includes("suitcase")) {
        response =
          "I found some excellent luggage options for you! Here are our top recommendations based on customer reviews and features:"
        products = mockProducts
      } else if (userMessage.toLowerCase().includes("backpack")) {
        response = "Looking for a travel backpack? Check out this highly-rated option:"
        products = [mockProducts[2]]
      } else if (userMessage.toLowerCase().includes("help") || userMessage.toLowerCase().includes("recommend")) {
        response =
          "I'd be happy to help you find the perfect luggage! I can show you our collection of premium suitcases, backpacks, and travel gear. What type of luggage are you interested in?"
      } else {
        response =
          "I can help you find luggage, suitcases, backpacks, and travel accessories. What are you shopping for today?"
      }

      updateCurrentConversation((conv) => ({
        ...conv,
        messages: [
          ...conv.messages,
          { role: "assistant", content: response, products: products.length > 0 ? products : undefined },
        ],
      }))
      setIsLoading(false)
    }, 1000)
  }

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden">
      <div
        className={`${
          isSidebarOpen ? "w-64" : "w-0"
        } flex-shrink-0 border-r border-border bg-card transition-all duration-300 overflow-hidden flex flex-col`}
      >
        <div className="p-4 border-b border-border flex-shrink-0">
          <Button
            onClick={createNewConversation}
            className="w-full justify-start gap-2 bg-transparent"
            variant="outline"
          >
            <MessageSquarePlus className="h-4 w-4" />
            New Chat
          </Button>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-2">
          {conversations.map((conv) => (
            <div
              key={conv.id}
              className={`group relative rounded-lg p-3 cursor-pointer transition-colors ${
                currentConversationId === conv.id
                  ? "bg-primary/10 border border-primary/20"
                  : "hover:bg-muted border border-transparent"
              }`}
              onClick={() => setCurrentConversationId(conv.id)}
            >
              <div className="flex items-center justify-between">
                <span className="text-sm truncate pr-2">{conv.title}</span>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
                  onClick={(e) => {
                    e.stopPropagation()
                    deleteConversation(conv.id)
                  }}
                >
                  <Trash2 className="h-3 w-3" />
                </Button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="border-b border-border bg-card px-6 py-4 flex-shrink-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Button variant="ghost" size="icon" onClick={() => setIsSidebarOpen(!isSidebarOpen)}>
                <Menu className="h-5 w-5" />
              </Button>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
                AI Shopping Assistant
              </h1>
            </div>
            <Button
              variant="outline"
              size="sm"
              className="gap-2 relative bg-transparent"
              onClick={() => setIsCartOpen(!isCartOpen)}
            >
              <ShoppingCart className="h-4 w-4" />
              <span>Cart</span>
              {cartItemCount > 0 && (
                <span className="absolute -top-2 -right-2 h-5 w-5 rounded-full bg-primary text-primary-foreground text-xs flex items-center justify-center animate-in zoom-in-0">
                  {cartItemCount}
                </span>
              )}
            </Button>
          </div>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {currentConversation.messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === "user" ? "justify-end" : "justify-start"} animate-in fade-in-0 slide-in-from-bottom-4`}
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <div className={`max-w-3xl ${message.role === "user" ? "w-auto" : "w-full"}`}>
                <div
                  className={`rounded-2xl px-6 py-4 ${
                    message.role === "user"
                      ? "bg-primary text-primary-foreground ml-auto max-w-md"
                      : "bg-muted text-foreground"
                  }`}
                >
                  <p className="whitespace-pre-wrap">{message.content}</p>
                </div>

                {message.type === "shipping-form" && (
                  <Card className="mt-4 p-6 border-2 border-primary/20 bg-card animate-in slide-in-from-bottom-4">
                    <div className="flex items-center gap-2 mb-4">
                      <Package className="h-5 w-5 text-primary" />
                      <h3 className="text-lg font-semibold">Shipping Information</h3>
                    </div>
                    <form onSubmit={handleShippingSubmit} className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <label className="text-sm font-medium">First Name</label>
                          <Input
                            required
                            placeholder="John"
                            value={shippingInfo.firstName}
                            onChange={(e) => setShippingInfo({ ...shippingInfo, firstName: e.target.value })}
                            className="bg-background"
                          />
                        </div>
                        <div className="space-y-2">
                          <label className="text-sm font-medium">Last Name</label>
                          <Input
                            required
                            placeholder="Doe"
                            value={shippingInfo.lastName}
                            onChange={(e) => setShippingInfo({ ...shippingInfo, lastName: e.target.value })}
                            className="bg-background"
                          />
                        </div>
                      </div>

                      <div className="space-y-2">
                        <label className="text-sm font-medium">Email</label>
                        <Input
                          required
                          type="email"
                          placeholder="john@example.com"
                          value={shippingInfo.email}
                          onChange={(e) => setShippingInfo({ ...shippingInfo, email: e.target.value })}
                          className="bg-background"
                        />
                      </div>

                      <div className="space-y-2">
                        <label className="text-sm font-medium">Address</label>
                        <Input
                          required
                          placeholder="123 Main St"
                          value={shippingInfo.address}
                          onChange={(e) => setShippingInfo({ ...shippingInfo, address: e.target.value })}
                          className="bg-background"
                        />
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <label className="text-sm font-medium">City</label>
                          <Input
                            required
                            placeholder="New York"
                            value={shippingInfo.city}
                            onChange={(e) => setShippingInfo({ ...shippingInfo, city: e.target.value })}
                            className="bg-background"
                          />
                        </div>
                        <div className="space-y-2">
                          <label className="text-sm font-medium">Zip Code</label>
                          <Input
                            required
                            placeholder="10001"
                            value={shippingInfo.zipCode}
                            onChange={(e) => setShippingInfo({ ...shippingInfo, zipCode: e.target.value })}
                            className="bg-background"
                          />
                        </div>
                      </div>

                      <Button type="submit" className="w-full" size="lg">
                        Continue to Payment
                      </Button>
                    </form>
                  </Card>
                )}

                {message.type === "payment-form" && (
                  <Card className="mt-4 p-6 border-2 border-primary/20 bg-card animate-in slide-in-from-bottom-4">
                    <div className="flex items-center gap-2 mb-4">
                      <CreditCard className="h-5 w-5 text-primary" />
                      <h3 className="text-lg font-semibold">Payment Details</h3>
                    </div>

                    {/* Order Summary */}
                    <div className="rounded-lg border border-border bg-muted/50 p-4 space-y-2 mb-6">
                      <h4 className="font-semibold text-sm">Order Summary</h4>
                      {cart.map((item) => (
                        <div key={item.id} className="flex justify-between text-sm">
                          <span className="text-muted-foreground">
                            {item.title} x{item.quantity}
                          </span>
                          <span className="font-medium">${(item.price * item.quantity).toFixed(2)}</span>
                        </div>
                      ))}
                      <div className="border-t border-border pt-2 flex justify-between font-semibold">
                        <span>Total</span>
                        <span className="text-primary text-lg">${cartTotal.toFixed(2)}</span>
                      </div>
                    </div>

                    <form onSubmit={handlePayment} className="space-y-4">
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Card Number</label>
                        <Input
                          required
                          placeholder="1234 5678 9012 3456"
                          value={paymentInfo.cardNumber}
                          onChange={(e) =>
                            setPaymentInfo({
                              ...paymentInfo,
                              cardNumber: formatCardNumber(e.target.value),
                            })
                          }
                          maxLength={19}
                          disabled={isProcessingPayment}
                          className="bg-background"
                        />
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <label className="text-sm font-medium">Expiry Date</label>
                          <Input
                            required
                            placeholder="MM/YY"
                            value={paymentInfo.expiryDate}
                            onChange={(e) =>
                              setPaymentInfo({
                                ...paymentInfo,
                                expiryDate: formatExpiryDate(e.target.value),
                              })
                            }
                            maxLength={5}
                            disabled={isProcessingPayment}
                            className="bg-background"
                          />
                        </div>
                        <div className="space-y-2">
                          <label className="text-sm font-medium">CVV</label>
                          <Input
                            required
                            placeholder="123"
                            value={paymentInfo.cvv}
                            onChange={(e) =>
                              setPaymentInfo({
                                ...paymentInfo,
                                cvv: e.target.value.replace(/\D/g, "").slice(0, 3),
                              })
                            }
                            maxLength={3}
                            type="password"
                            disabled={isProcessingPayment}
                            className="bg-background"
                          />
                        </div>
                      </div>

                      <div className="flex items-center gap-2 text-sm text-muted-foreground bg-muted/50 p-3 rounded-lg">
                        <Lock className="h-4 w-4" />
                        <span>Your payment information is secure and encrypted</span>
                      </div>

                      <Button type="submit" className="w-full gap-2" size="lg" disabled={isProcessingPayment}>
                        {isProcessingPayment ? (
                          <>
                            <div className="h-5 w-5 animate-spin rounded-full border-2 border-background border-t-transparent" />
                            Processing Payment...
                          </>
                        ) : (
                          <>
                            <CreditCard className="h-5 w-5" />
                            Pay ${cartTotal.toFixed(2)}
                          </>
                        )}
                      </Button>
                    </form>
                  </Card>
                )}

                {message.type === "success" && (
                  <div className="mt-4 p-8 rounded-2xl border-2 border-green-500/30 bg-green-500/5 animate-in zoom-in-95 fade-in-0 duration-500">
                    <div className="flex flex-col items-center text-center space-y-4">
                      <div className="rounded-full bg-green-500/10 p-4 animate-in zoom-in-0 duration-700">
                        <Check className="h-12 w-12 text-green-500" />
                      </div>
                      <h3 className="text-xl font-bold text-green-600 dark:text-green-400">Order Confirmed!</h3>
                      <p className="text-muted-foreground max-w-md">
                        Thank you for your purchase! Your order is being processed.
                      </p>
                    </div>
                  </div>
                )}

                {message.products && message.products.length > 0 && (
                  <div className="mt-4 space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {message.products.map((product, pIndex) => (
                        <Card
                          key={product.id}
                          className="overflow-hidden border-border hover:border-primary/50 transition-all duration-300 hover:shadow-lg group animate-in fade-in-0 slide-in-from-bottom-4"
                          style={{ animationDelay: `${pIndex * 100}ms` }}
                        >
                          <div className="relative overflow-hidden bg-muted">
                            <img
                              src={product.image || "/placeholder.svg"}
                              alt={product.title}
                              className="h-48 w-full object-cover transition-transform duration-500 group-hover:scale-110"
                            />
                          </div>
                          <div className="p-4 space-y-3">
                            <h3 className="font-semibold text-foreground line-clamp-2 min-h-[3rem]">{product.title}</h3>
                            <p className="text-sm text-muted-foreground line-clamp-2">{product.description}</p>
                            <div className="flex items-center justify-between pt-2">
                              <span className="text-2xl font-bold text-primary">${product.price}</span>
                              <Button size="sm" className="gap-2 group/btn" onClick={() => addToCart(product)}>
                                <Plus className="h-4 w-4 transition-transform group-hover/btn:rotate-90" />
                                Add to Cart
                              </Button>
                            </div>
                          </div>
                        </Card>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start animate-in fade-in-0">
              <div className="bg-muted rounded-2xl px-6 py-4">
                <div className="flex gap-2">
                  <div className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce" />
                  <div
                    className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce"
                    style={{ animationDelay: "0.2s" }}
                  />
                  <div
                    className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce"
                    style={{ animationDelay: "0.4s" }}
                  />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="border-t border-border bg-card p-6 flex-shrink-0">
          <form
            onSubmit={(e) => {
              e.preventDefault()
              handleSendMessage()
            }}
            className="flex gap-4"
          >
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask for products or type 'checkout' to complete your order..."
              className="flex-1 bg-background"
              disabled={isLoading || isProcessingPayment}
            />
            <Button
              type="submit"
              size="icon"
              className="shrink-0"
              disabled={isLoading || !input.trim() || isProcessingPayment}
            >
              <Send className="h-5 w-5" />
            </Button>
          </form>
          <p className="text-xs text-muted-foreground mt-2 text-center">
            Try: "Show me luggage" or "Add product 1 to cart" or "checkout"
          </p>
        </div>
      </div>

      {/* Cart Drawer */}
      {isCartOpen && (
        <div className="fixed inset-0 z-50 animate-in fade-in-0 duration-300">
          <div className="absolute inset-0 bg-black/60" onClick={() => setIsCartOpen(false)} />
          <div className="absolute right-0 top-0 h-full w-full max-w-md bg-card shadow-2xl animate-in slide-in-from-right-full duration-300">
            <div className="flex h-full flex-col">
              <div className="flex items-center justify-between border-b border-border p-4">
                <h2 className="text-xl font-semibold text-foreground">Your Cart</h2>
                <Button variant="ghost" size="icon" onClick={() => setIsCartOpen(false)}>
                  <X className="h-5 w-5" />
                </Button>
              </div>

              {cart.length === 0 ? (
                <div className="flex flex-1 items-center justify-center text-muted-foreground">Your cart is empty</div>
              ) : (
                <>
                  <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    {cart.map((item, index) => (
                      <Card
                        key={item.id}
                        className="overflow-hidden border-border animate-in fade-in-0 slide-in-from-right-4"
                        style={{ animationDelay: `${index * 50}ms` }}
                      >
                        <div className="flex gap-4 p-4">
                          <img
                            src={item.image || "/placeholder.svg"}
                            alt={item.title}
                            className="h-20 w-20 rounded-lg object-cover bg-muted"
                          />
                          <div className="flex-1 space-y-2">
                            <h3 className="font-semibold text-foreground line-clamp-2">{item.title}</h3>
                            <div className="flex items-center gap-2">
                              <Button
                                variant="outline"
                                size="icon"
                                className="h-7 w-7 bg-transparent"
                                onClick={() => updateQuantity(item.id, -1)}
                              >
                                <Minus className="h-4 w-4" />
                              </Button>
                              <span className="w-8 text-center font-medium">{item.quantity}</span>
                              <Button
                                variant="outline"
                                size="icon"
                                className="h-7 w-7 bg-transparent"
                                onClick={() => updateQuantity(item.id, 1)}
                              >
                                <Plus className="h-4 w-4" />
                              </Button>
                            </div>
                            <span className="font-semibold text-foreground">
                              ${(item.price * item.quantity).toFixed(2)}
                            </span>
                          </div>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => removeFromCart(item.id)}
                            className="shrink-0 hover:bg-destructive hover:text-destructive-foreground"
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        </div>
                      </Card>
                    ))}
                  </div>
                  <div className="border-t border-border p-4 space-y-4">
                    <div className="flex items-center justify-between text-lg">
                      <span className="font-semibold text-foreground">Total</span>
                      <span className="text-2xl font-bold text-foreground">${cartTotal.toFixed(2)}</span>
                    </div>
                    <Button className="w-full" size="lg" onClick={startCheckoutFlow}>
                      Proceed to Checkout
                    </Button>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
