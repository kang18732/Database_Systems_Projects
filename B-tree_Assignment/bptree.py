import argparse
import collections
import math


class Node:
    def __init__(self):
        self.num_of_keys = 0
        self.pairs = []
        self.next = None
        self.is_leaf = True

    def insert_leaf(self, new_pair) -> bool:    # new_pair는 새로운 [key,value] pair
        if self.num_of_keys == 0:               # 비어있는 노드라면 pairs에 바로 new_pair를 append
            self.pairs.append(new_pair)
        else:                                   # 비어있지 않다면 new_pair가 들어갈 위치를 찾음
            for i, pair in enumerate(self.pairs):
                if new_pair[0] < pair[0]:       # 새로운 키가 기존 키보다 작으면 그 위치에 new_pair 삽입
                    self.pairs = self.pairs[:i] + [new_pair] + self.pairs[i:]
                    self.num_of_keys += 1
                    return True
                elif new_pair[0] == pair[0]:    # 중복키가 존재하면 False를 return하고 함수 종료
                    return False
            self.pairs.append(new_pair)         # 새로운 키가 가장 크면 마지막에 append
        self.num_of_keys += 1
        return True


class BPTree:
    def __init__(self, degree):
        self.root = Node()
        self.degree = degree

    def split_index(self, stack, node: Node):
        parent = None
        if stack:
            parent = stack.pop()    # node의 부모 노드를 스택을 통해 할당
        else:
            parent = Node()         # 부모가 없다면 새로 생성

        mid = self.degree // 2

        new_sibling = Node()                        # 오른쪽 형제 노드 생성
        new_sibling.is_leaf = False
        new_sibling.next = node.next                # node가 가리키던 rightmost child를 new_sibling이 가리키도록 함
        new_sibling.pairs = node.pairs[mid + 1:]    # 기준 키를 제외한 오른쪽 반을 new_sibling에 넘김
        new_sibling.num_of_keys = len(new_sibling.pairs)

        mid_key = node.pairs[mid][0]

        if parent.num_of_keys == 0:                 # 새로 생성된 부모인 경우
            parent.pairs.append([mid_key, node])        # mid_key를 올리고 left child로 node를 가리키게 함
            parent.next = new_sibling                   # 부모의 rightmost child를 new_sibling으로 변경
        else:                                       # 부모가 원래 존재하는 경우
            for i, pair in enumerate(parent.pairs):
                if mid_key < pair[0]:
                    parent.pairs[i][1] = new_sibling    # 기존에 node를 가리키던 포인터가 new_sibling을 가리키도록 바꿈
                    parent.pairs = parent.pairs[:i] + [[mid_key, node]] + parent.pairs[i:] # node를 가리키는 새로운 pair 삽입
                    break
                elif i == len(parent.pairs) - 1:        # mid_key가 가장 큰 경우
                    parent.pairs.append([mid_key, node])    # 가장 마지막에 새로운 pair 삽입
                    parent.next = new_sibling               # 부모의 rightmost child를 new_sibling으로 지정
                    break
        parent.num_of_keys += 1

        node.next = node.pairs[mid][1]              # node의 rightmost child를 기준 키가 가리키던 left child로 변경
        node.pairs = node.pairs[:mid]               # 기준 키를 제외한 나머지 왼쪽 반을 node가 갖도록 함
        node.num_of_keys = len(node.pairs)

        if parent.is_leaf:                          # 새로운 부모면 root로 지정
            parent.is_leaf = False
            self.root = parent

        if parent.num_of_keys == self.degree:       # 부모 노드도 키 개수 초과하면 재귀로 함수 호출
            self.split_index(stack, parent)

    def split_leaf(self, parent: Node, node: Node):
        if parent is None:  # root가 리프노드인 경우에 부모가 존재하지 않으므로 새로 생성
            parent = Node()

        new_sibling = Node()            # 새로운 오른쪽 형제 노드를 생성
        new_sibling.next = node.next    # node가 가리키던 right sibling을 new_sibling이 가리키도록 함
        node.next = new_sibling         # node는 이제 새로 만들어진 new_sibling을 가리킴

        mid = self.degree // 2
        mid_key = node.pairs[mid][0]    # 부모 노드로 올라갈 키 지정 (degree/2을 내림한 값이 기준)

        if parent.num_of_keys == 0:     # 부모가 새로 생성된 경우
            parent.pairs.append([mid_key, node])    # mid_key를 올리고 left child로 node를 가리키게 함
            parent.next = new_sibling               # 부모의 rightmost child는 new_sibling이 됨
        else:                           # 부모가 원래 있던 경우
            for i, pair in enumerate(parent.pairs):
                if mid_key < pair[0]:
                    parent.pairs[i][1] = new_sibling    # 기존에 node를 가리키던 포인터가 new_sibling을 가리키도록 바꿈
                    parent.pairs = parent.pairs[:i] + [[mid_key, node]] + parent.pairs[i:]  # node를 가리키는 새로운 pair 삽입
                    break
                elif i == len(parent.pairs) - 1:        # mid_key가 가장 큰 경우
                    parent.pairs.append([mid_key, node])    # 가장 마지막에 새로운 pair 삽입
                    parent.next = new_sibling               # rightmost child를 new_sibling으로 지정
                    break
        parent.num_of_keys += 1

        new_sibling.pairs = node.pairs[mid:]                # node의 오른쪽 반을 new_sibling이 갖도록 함
        new_sibling.num_of_keys = len(new_sibling.pairs)
        node.pairs = node.pairs[:mid]                       # node를 반으로 줄임 (왼쪽 반만 갖도록)
        node.num_of_keys = len(node.pairs)

        if parent.is_leaf:              # 새로 부모를 생성하면 초기 상태이므로 is_leaf가 True
            parent.is_leaf = False      # 리프 노드가 아니므로 False로 바꿔줌
            self.root = parent          # 새 부모가 root가 되므로 root에 parent을 할당

    def insert(self, new_pair):
        node = self.root
        prev = None         # node의 부모 노드를 가리키는 변수 (초기에는 None)
        stack = []          # root 노드부터 순차적으로 index 노드들을 저장할 비어있는 스택을 생성
        while not node.is_leaf:                  # 리프노드에 도달할 때까지 반복
            for i, pair in enumerate(node.pairs):
                if new_pair[0] == pair[0]:       # 중복된 키면 함수 종료
                    return
                elif new_pair[0] < pair[0]:
                    stack.append(node)
                    node = pair[1]               # node에 pair가 가리키는 left child를 할당
                    break
                elif i == len(node.pairs) - 1:   # 새로운 키가 가장 커서 끝에 다다른 경우
                    stack.append(node)
                    node = node.next             # node에 rightmost child를 할당
                    break
        if not node.insert_leaf(new_pair):     # leaf 레벨에서 삽입이 실패하면 함수 종료
            return

        if stack:
            prev = stack.pop()                  # prev에 leaf 노드의 parent 노드 할당
        if node.num_of_keys == self.degree:
            self.split_leaf(prev, node)         # node의 키 개수가 초과되면 split
            if prev and prev.num_of_keys == self.degree:
                self.split_index(stack, prev)   # parent 노드도 키 개수 초과하면 split

    def serialize(self, idx_file: str):
        f = open(idx_file, 'w')
        f.write(str(self.degree))
        f.write('\n')

        node = self.root
        # 트리의 가장 왼쪽 리프 노드로 이동
        while node.pairs and not node.is_leaf:
            node = node.pairs[0][1]

        # 가장 왼쪽 리프 노드부터 가장 오른쪽 리프 노드까지 모든 key,value를 한 줄씩 저장
        while node:
            for key, value in node.pairs:
                f.write(str(key))
                f.write(',')
                f.write(str(value))
                f.write('\n')
            node = node.next
        f.close()

    def bulk_split_leaf(self, parent: Node, node: Node) -> Node:
        if parent is None:
            parent = Node()

        new_sibling = Node()        # 오른쪽 형제 노드 생성 <- 이 노드가 rightmost leaf node가 됨
        node.next = new_sibling     # node의 오른쪽 형제를 new_sibling으로 변경

        mid = self.degree // 2
        mid_key = node.pairs[mid][0]

        parent.pairs.append([mid_key, node])    # for문 돌 필요 없이 항상 부모의 마지막에 pair가 추가됨
        parent.next = new_sibling               # 부모의 rightmost child는 new_sibling으로 바뀜
        parent.num_of_keys += 1

        new_sibling.pairs = node.pairs[mid:]
        new_sibling.num_of_keys = len(new_sibling.pairs)
        node.pairs = node.pairs[:mid]
        node.num_of_keys = len(node.pairs)

        if parent.is_leaf:
            parent.is_leaf = False
            self.root = parent

        return new_sibling

    def bulk_split_index(self, stack, node: Node):
        parent = None
        if stack:
            parent = stack.pop()
        else:
            parent = Node()

        mid = self.degree // 2

        new_sibling = Node()
        new_sibling.is_leaf = False
        new_sibling.next = node.next
        new_sibling.pairs = node.pairs[mid + 1:]
        new_sibling.num_of_keys = len(new_sibling.pairs)

        mid_key = node.pairs[mid][0]

        parent.pairs.append([mid_key, node])
        parent.next = new_sibling
        parent.num_of_keys += 1

        node.next = node.pairs[mid][1]
        node.pairs = node.pairs[:mid]
        node.num_of_keys = len(node.pairs)

        if parent.is_leaf:
            parent.is_leaf = False
            self.root = parent

        if parent.num_of_keys == self.degree:
            self.bulk_split_index(stack, parent)

    def delete_leaf(self, parent: Node, node: Node, key: int, idx: int):
        min_keys = math.ceil(self.degree / 2) - 1   # root를 제외한 노드가 갖는 최소 키 개수

        if not node.is_leaf:                        # 리프 노드에 도달할 때까지 재귀로 함수 호출
            for i, pair in enumerate(node.pairs):
                if key < pair[0]:
                    successor = self.delete_leaf(node, pair[1], key, i)     # 현재 노드, 자식 노드, 키, 자식 노드의 index를 넘겨줌
                    self.replace(parent, key, successor)                    # 부모 노드에서 삭제된 키가 존재하면 successor로 대체
                    self.balance_tree(parent, node, key)                    # 부모와 현재 노드를 넘겨서 tree를 balance시킴
                    return successor
                elif i == len(node.pairs) - 1:
                    successor = self.delete_leaf(node, node.next, key, i + 1)
                    self.replace(parent, key, successor)
                    self.balance_tree(parent, node, key)
                    return successor

        found = False
        pos = -1
        for i, pair in enumerate(node.pairs):
            if key == pair[0]:
                found = True
                pos = i
                break
        if not found:
            return

        replace_key = None
        if node.num_of_keys > 1 and pos < len(node.pairs) - 1:
            replace_key = node.pairs[pos + 1][0]

        node.pairs = node.pairs[:pos] + node.pairs[pos + 1:]    # 노드에서 키 삭제
        node.num_of_keys -= 1

        if node is self.root:
            return

        if node.num_of_keys >= min_keys:    # 삭제 이후에도 키 개수가 충분한 경우
            if pos == 0 and idx > 0:                            # 가장 첫번째 키가 삭제됐으면 부모의 키도 삭제되어야함
                parent.pairs[idx - 1][0] = node.pairs[0][0]     # 삭제된 키의 다음 키로 부모 키를 대체함
        else:                               # 키 개수가 부족한 경우
            left_neighbor, right_neighbor = None, None
            if idx > 0:                         # delete_leaf 함수의 마지막 인자 idx(부모 노드에서 현재 노드의 위치) 활용
                left_neighbor = parent.pairs[idx - 1][1]    # 왼쪽 키의 left child가 left_neighbor
            if idx < len(parent.pairs) - 1:
                right_neighbor = parent.pairs[idx + 1][1]   # 오른쪽 키의 left child가 right_neighbor
            elif idx == len(parent.pairs) - 1:
                right_neighbor = parent.next                # 더이상 오른쪽 키가 없다면 부모의 rightmost child가 right_neighbor

            # Redistribution
            if left_neighbor and left_neighbor.num_of_keys > min_keys:  # 왼쪽 형제가 존재하고 키의 개수가 많은 경우
                node.pairs = [left_neighbor.pairs[-1]] + node.pairs     # 왼쪽 형제의 마지막 키를 가져옴
                node.num_of_keys += 1
                left_neighbor.pairs = left_neighbor.pairs[:-1]          # 왼쪽 형제의 마지막 키 삭제
                left_neighbor.num_of_keys -= 1
                parent.pairs[idx - 1][0] = node.pairs[0][0]             # 부모 노드의 키 업데이트
            elif right_neighbor and right_neighbor.num_of_keys > min_keys:  # 오른쪽 형제가 존재하고 키의 개수가 많은 경우
                if node.num_of_keys == 0:                           # 노드가 비어있으면 대체키는 오른쪽 형제의 첫번째 키
                    replace_key = right_neighbor.pairs[0][0]
                node.pairs.append(right_neighbor.pairs[0])          # 오른쪽 형제의 첫번째 키를 추가
                node.num_of_keys += 1
                right_neighbor.pairs = right_neighbor.pairs[1:]     # 오른쪽 형제의 첫번째 키 삭제
                right_neighbor.num_of_keys -= 1
                parent.pairs[idx][0] = right_neighbor.pairs[0][0]   # 부모 노드의 키 업데이트
            # Merge
            elif left_neighbor:                 # 왼쪽 형제의 키 개수가 충분하지 않은 경우 (node를 왼쪽 형제에 흡수시킴)
                left_neighbor.next = node.next      # node의 rightmost child는 이제 왼쪽 형제의 rightmost child
                left_neighbor.pairs = left_neighbor.pairs + node.pairs
                left_neighbor.num_of_keys += node.num_of_keys
                if idx < len(parent.pairs):         # node가 부모의 rightmost child가 아닌 경우
                    parent.pairs[idx][1] = left_neighbor                    # node를 가리키던 포인터가 왼쪽 형제를 가리키도록 변경
                else:                               # node가 부모의 rightmost child인 경우
                    parent.next = left_neighbor                             # 부모의 rightmost child를 왼쪽 형제로 변경
                parent.pairs = parent.pairs[:idx - 1] + parent.pairs[idx:]  # 부모 노드에서 기존에 왼쪽 형제 가리키던 pair 삭제
                parent.num_of_keys -= 1

                if parent == self.root and parent.num_of_keys == 0:
                    self.root = left_neighbor                               # 부모가 비었는데 root였다면 root를 새로 지정
            elif right_neighbor:                # 오른쪽 형제의 키 개수가 충분하지 않은 경우 (오른쪽 형제를 node에 흡수시킴)
                if node.num_of_keys == 0:
                    replace_key = right_neighbor.pairs[0][0]
                node.next = right_neighbor.next                 # 오른쪽 형제의 rightmost child는 이제 node의 rightmost child
                node.pairs = node.pairs + right_neighbor.pairs
                node.num_of_keys += right_neighbor.num_of_keys
                if idx == len(parent.pairs) - 1:        # node가 부모의 오른쪽에서 두번째 child인 경우
                    parent.next = node                          # 부모의 rightmost child를 node로 변경
                else:                                   # node가 부모의 오른쪽에서 세번째~마지막 child인 경우
                    parent.pairs[idx + 1][1] = node             # 오른쪽 형제를 가리키던 포인터를 node로 바꿈
                parent.pairs = parent.pairs[:idx] + parent.pairs[idx + 1:]  # 기존에 오른쪽 형제 가리키던 pair 삭제
                parent.num_of_keys -= 1

                if parent == self.root and parent.num_of_keys == 0:
                    self.root = node                                        # 부모가 비었는데 root였다면 root를 새로 지정

        return replace_key

    def replace(self, parent: Node, key: int, successor):
        if parent and successor is not None:
            for i, pair in enumerate(parent.pairs):
                if pair[0] == key:
                    parent.pairs[i][0] = successor      # 삭제된 키를 찾으면 successor로 대체하고 종료
                    return

    def balance_tree(self, parent: Node, node: Node, key: int):
        min_keys = math.ceil(self.degree / 2) - 1
        if not parent or node.num_of_keys >= min_keys:  # 부모가 없거나 노드의 키 개수가 충분하면 함수 종료
            return

        idx = -1
        for i, pair in enumerate(parent.pairs):     # 부모 노드에서 현재 노드의 index를 idx에 저장
            if pair[1] == node:
                idx = i
                break
            if parent.next == node:                 # 부모의 rightmost child면 부모의 길이가 index가 됨
                idx = len(parent.pairs)
                break

        left_neighbor, right_neighbor = None, None
        if idx > 0:
            left_neighbor = parent.pairs[idx - 1][1]
        if idx < len(parent.pairs) - 1:
            right_neighbor = parent.pairs[idx + 1][1]
        elif idx == len(parent.pairs) - 1:
            right_neighbor = parent.next

        # Redistribution - Rotate하듯이 키를 옮김
        if left_neighbor and left_neighbor.num_of_keys > min_keys:
            # idx를 이용해서 왼쪽 형제의 키를 부모로 옮기고 부모의 키를 node로 옮김
            # 왼쪽 형제의 마지막 키를 가져오므로 왼쪽 형제의 rightmost child가 node의 leftmost child가 됨
            node.pairs = [[parent.pairs[idx - 1][0], left_neighbor.next]] + node.pairs  # 부모 노드의 키를 node로 옮김
            left_neighbor.next = left_neighbor.pairs[-1][1]         # 왼쪽 형제의 rightmost child를 오른쪽에서 두번째 child로 변경
            parent.pairs[idx - 1][0] = left_neighbor.pairs[-1][0]   # 왼쪽 형제의 마지막 키를 부모 노드로 옮김
            left_neighbor.pairs = left_neighbor.pairs[:-1]
            node.num_of_keys += 1
            left_neighbor.num_of_keys -= 1
        elif right_neighbor and right_neighbor.num_of_keys > min_keys:
            node.pairs.append([parent.pairs[idx][0], node.next])
            node.next = right_neighbor.pairs[0][1]
            parent.pairs[idx][0] = right_neighbor.pairs[0][0]
            right_neighbor.pairs = right_neighbor.pairs[1:]
            node.num_of_keys += 1
            right_neighbor.num_of_keys -= 1
        # Merge
        elif left_neighbor:     # node가 왼쪽 형제 흡수
            # 부모의 키와 왼쪽 형제의 rightmost child를 새로운 pair로 묶어서 왼쪽 형제 마지막에 추가
            left_neighbor.pairs.append([parent.pairs[idx - 1][0], left_neighbor.next])
            node.pairs = left_neighbor.pairs + node.pairs               # node 앞에 왼쪽 형제 추가
            node.num_of_keys = len(node.pairs)
            parent.pairs = parent.pairs[:idx - 1] + parent.pairs[idx:]  # 부모에서 index 삭제
            parent.num_of_keys -= 1
            if parent.num_of_keys == 0 and parent == self.root:     # 부모가 비었는데 root였으면 root를 node로 지정
                self.root = node
        elif right_neighbor:
            node.pairs.append([parent.pairs[idx][0], node.next])
            node.next = right_neighbor.next
            node.pairs.extend(right_neighbor.pairs)
            node.num_of_keys = len(node.pairs)
            if idx == len(parent.pairs) - 1:
                parent.next = node
            else:
                parent.pairs[idx + 1][1] = node
            parent.pairs = parent.pairs[:idx] + parent.pairs[idx + 1:]
            parent.num_of_keys -= 1
            if parent.num_of_keys == 0 and parent == self.root:
                self.root = node

    def deserialize(self, idx_file: str):
        f = open(idx_file, 'r')
        degree = int(f.readline())          # degree부터 읽은 다음 degree를 설정함
        self.degree = degree

        rightmost = self.root               # 새로운 키는 항상 가장 큰 키이므로 무조건 rightmost leaf node에 삽입됨
        parent = None

        while True:
            line = f.readline()
            if not line:
                break
            rightmost.pairs.append(list(map(int, line.split(','))))     # 읽은 key,value를 리스트 형태로 저장
            rightmost.num_of_keys += 1

            stack = []

            if rightmost.num_of_keys == self.degree:    # rightmost leaf가 키 최대 개수 초과하면 split 진행
                node = self.root
                while not node.is_leaf:
                    stack.append(node)
                    node = node.next            # rightmost leaf의 부모로 이동하려면 계속 rightmost child로 이동하면 됨
                if stack:
                    parent = stack.pop()
                rightmost = self.bulk_split_leaf(parent, rightmost) # leaf 레벨에서 split 진행하고 rightmost leaf return함
                if parent and parent.num_of_keys == self.degree:    # 부모도 키 개수 초과하면 index 레벨에서 split 진행
                    self.bulk_split_index(stack, parent)

        f.close()

    def search(self, node: Node, key: int) -> bool:
        if not node.is_leaf:                        # 리프 노드에 도달할 때까지 재귀로 탐색
            for i, pair in enumerate(node.pairs):   # 노드의 모든 키 출력
                if i < len(node.pairs) - 1:
                    print(pair[0], end=',')
                else:
                    print(pair[0])

            for i, pair in enumerate(node.pairs):
                if key < pair[0]:                   # 탐색할 키가 노드에 있는 키보다 작으면 left child로 이동
                    return self.search(pair[1], key)
                elif i == len(node.pairs) - 1:      # 탐색할 키가 가장 크면 rightmost child로 이동
                    return self.search(node.next, key)

        for i, pair in enumerate(node.pairs):       # 리프 노드에 키가 있는지 확인하고, 없으면 True 있으면 False return
            if key == pair[0]:
                print(pair[1])
                return True
        return False

    def range_search(self, node: Node, start: int, end: int):
        if start > end:                     # start가 end보다 크면 탐색 조건이 성립하지 않음 (예외 처리)
            print("Lower bound bigger than Upper bound")
            return

        if not node.is_leaf:                # search 함수와 마찬가지
            for i, pair in enumerate(node.pairs):
                if start < pair[0]:
                    self.range_search(pair[1], start, end)
                    return
                elif i == len(node.pairs) - 1:
                    self.range_search(node.next, start, end)
                    return

        found = False                       # range에 맞는 값을 발견하면 True를 할당하기 위한 초기 설정
        for i, pair in enumerate(node.pairs):
            if start <= pair[0] <= end:     # 범위에 맞는 값 발견하면 거기서부터 순차적으로 출력
                print(f"{pair[0]},{pair[1]}")
                found = True

        node = node.next                    # right sibling으로 계속 넘어감
        while node:
            for i, pair in enumerate(node.pairs):
                if start <= pair[0] <= end:
                    print(f"{pair[0]},{pair[1]}")
                    found = True
                elif pair[0] > end:         # 만약 키가 end보다 크면 더 이상 탐색할 필요 없으므로 함수 종료
                    if not found:
                        print("NOT FOUND")
                    return
            node = node.next

        if not found:                       # found가 False면 못 찾은 것이므로 NOT FOUND 출력
            print("NOT FOUND")


parser = argparse.ArgumentParser()
parser.add_argument('--create', '-c', nargs=2)
parser.add_argument('--insert', '-i', nargs=2)
parser.add_argument('--delete', '-d', nargs=2)
parser.add_argument('--search', '-s', nargs=2)
parser.add_argument('--rsearch', '-r', nargs=3)

args = parser.parse_args()

if args.create:
    file_name = args.create[0]
    degree = args.create[1]
    if int(degree) < 3:
        print("Degree must be greater than 2")
    f = open(file_name, 'w')
    f.write(degree)
    f.close()
elif args.insert:
    idx_file = args.insert[0]
    input_data = args.insert[1]

    tree = BPTree(0)
    tree.deserialize(idx_file)

    f = open(input_data, 'r')
    while True:
        line = f.readline()
        if not line:
            break
        tree.insert(list(map(int, line.split(','))))
    f.close()

    tree.serialize(idx_file)
elif args.delete:
    idx_file = args.delete[0]
    del_data = args.delete[1]

    tree = BPTree(0)
    tree.deserialize(idx_file)

    f = open(del_data, 'r')
    while True:
        line = f.readline()
        if not line:
            break
        tree.delete_leaf(None, tree.root, int(line), -1)
    f.close()

    tree.serialize(idx_file)
elif args.search:
    idx_file = args.search[0]
    key = int(args.search[1])

    tree = BPTree(0)
    tree.deserialize(idx_file)

    if not tree.search(tree.root, key):
        print("NOT FOUND")
elif args.rsearch:
    idx_file = args.rsearch[0]
    start = int(args.rsearch[1])
    end = int(args.rsearch[2])

    tree = BPTree(0)
    tree.deserialize(idx_file)

    tree.range_search(tree.root, start, end)