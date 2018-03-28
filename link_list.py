class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def create_llist(l):
    """
    正序创建链表
    """
    head = now_node = None
    for value in l:
        new_node = ListNode(value)
        if not now_node:
            head = now_node = new_node
        now_node.next = new_node
        now_node = new_node
    return head


def create_llist_reverse(l):
    """
    倒序创建链表
    """
    head = None
    for value in l:
        new_node = ListNode(value)
        if not head:
            head = new_node
        else:
            new_node.next = head
            head = new_node
    return head


def print_llist(ll):
    l = []
    while True:
        l.append(ll.val)
        if not ll.next:
            break
        ll = ll.next
    print(l)


def reverse_llist(ll):
    """
    反转链表
    """
    head = None
    while True:
        new_node = ListNode(ll.val)
        if not head:
            head = new_node
        else:
            new_node.next = head
            head = new_node

        if not ll.next:
            break
        ll = ll.next
    return head
