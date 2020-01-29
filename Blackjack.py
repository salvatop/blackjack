# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ["",""]
score = [0,0]


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
       
# define hand class
class Hand:        
    def __init__(self):
        self.Hand = []
        
    def __str__(self):
        self.txt = "Hand contains"
        for card in self.Hand:
            self.txt += " " +str(card)
        return self.txt 

    def add_card(self, card):
        self.Hand.append(card)

    def get_value(self):
        self.value = 0
        self.A = False
        for card in self.Hand:
            if card.get_rank() == "A" and self.value +11 <= 21:
                self.value += VALUES[card.get_rank()] +10
                self.A = True
            else:
                self.value += VALUES[card.get_rank()] 
                
        if self.A and self.value > 21:
            self.value -= 10
        return self.value     

    def draw(self, canvas, pos):
         for card in self.Hand:
            card.draw(canvas, pos)
            pos[0] += 50
    
# define deck class 
class Deck:
    def __init__(self):
        self.Deck = []
        for s in SUITS:
            for r in RANKS:
                self.Deck.append(Card(s,r))

    def shuffle(self):
        random.shuffle(self.Deck) 

    def deal_card(self):
        return self.Deck.pop()

    def __str__(self):        
        self.Deck
        self.txt = "Deck contains"
        for i in self.Deck:
            self.txt += " " + str(i)
        return self.txt

#define event handlers for buttons
def deal():
    global in_play, player, dealer, deck, outcome, score
    if in_play:
        score[0] += 1
    outcome = ["","Hit or Stand?"]
    deck = Deck()
    deck.shuffle()
    
    player = Hand()
    dealer = Hand()
    
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    print "Player", player
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    #print "Dealer", dealer
    
    in_play = True

def hit():
    global outcome, in_play, player, score, deck
    
    if in_play and player.get_value() <= 21:
        player.add_card(deck.deal_card())
        print "Player", player
        print "Total", player.get_value()
        outcome[1] = "Hit or stand?"
        if player.get_value() > 21:
            outcome[1] = "Player have busted! New deal?"
            score[0] += 1
            print outcome[1]
            in_play = False       

def stand():
    global outcome, in_play, player, dealer, score, deck
    while in_play:
         if dealer.get_value() <= player.get_value()and dealer.get_value() <= 21:
            dealer.add_card(deck.deal_card())
            print "Dealer", dealer
            print "Total", dealer.get_value()
            outcome[1] = "Player Stand"
            print outcome[1]
         else:
            if dealer.get_value() >= player.get_value()and dealer.get_value() <= 21:
                outcome[0] =  " " + " Hand Total " + str(dealer.get_value()) + " " +"Dealer Win! New deal?"
                print outcome[0]
                score[0] += 1
                in_play = False
            else:
                outcome[0] = " " + " Hand Total " + str(dealer.get_value()) + " " + "Dealer have busted, Player Win! New deal?"
                print outcome[0]
                score[1] += 1
                in_play = False
            
# draw handler    
def draw(canvas):
    global outcome, player, dealer, score
    canvas.draw_text('BLACKJACK', (150,40), 45, 'Black')   
    s1 = score[0]
    s2 = score[1]
    scores = "Dealer : " + str(s1) + "   " + "Player : " + str(s2)
    canvas.draw_text (str(scores), (460,20), 15, 'Black')
    
    canvas.draw_text('PLAYER : ', (50,260), 25, 'White')
    player_txt = " " + " Hand Total " + str(player.get_value()) + " " + outcome[1]
    canvas.draw_text(player_txt, (160,260), 15, 'White')    
    player.draw(canvas, [50, 280])

    canvas.draw_text('DEALER : ', (50,90), 25, 'White')
    dealer_txt = "  "  + outcome[0]
    canvas.draw_text(dealer_txt, (160,90), 15, 'White')
    dealer.draw(canvas, [50, 110])
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (87,158), CARD_BACK_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 400)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_label("")
frame.add_label("BLACKJACK RULES:")
frame.add_label("")
frame.add_label("The players plays against a dealer with the goal of building a hand whose cards have a total value that is higher than the value of the dealer's hand, but not over 21.") 
frame.add_label("")
frame.add_label("An ace may be valued as either 1 or 11 (player's choice), kings, queens and jacks are valued at 10 and the value of the remaining cards corresponds to their number.")
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
